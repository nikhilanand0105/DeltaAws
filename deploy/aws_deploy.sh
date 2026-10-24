#!/usr/bin/env bash
# ==============================================================================
# Automated One-Click AWS Deployment Script for Delta Trading Bot
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
STACK_NAME="delta-trading-bot-stack"
REGION="${AWS_REGION:-${AWS_DEFAULT_REGION:-ap-south-1}}"

echo "=========================================================="
echo " AWS Cloud Architecture Deployment Automation"
echo " Course: BCSE355L - Cloud Architecture Design (2026-27)"
echo " Project: Delta Exchange Algorithmic Trading Bot"
echo " Target Stack: $STACK_NAME"
echo " Target Region: $REGION"
echo "=========================================================="

# 1. Verify AWS CLI Authentication (ensuring non-root identity)
echo "[STEP 1/6] Verifying AWS CLI authentication..."
CALLER_IDENTITY=$(aws sts get-caller-identity --output json)
ACCOUNT_ID=$(echo "$CALLER_IDENTITY" | jq -r '.Account')
USER_ARN=$(echo "$CALLER_IDENTITY" | jq -r '.Arn')

echo "[SUCCESS] Authenticated as: $USER_ARN (Account: $ACCOUNT_ID)"

if [[ "$USER_ARN" == *":root" ]]; then
    echo "[WARN] Active AWS CLI identity is ROOT. Consider using an IAM deployment user (e.g. da3-deployer)."
fi

# 2. Discover Default VPC and Public Subnet
echo "[STEP 2/6] Discovering default VPC and public subnet in $REGION..."
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --region "$REGION" --query "Vpcs[0].VpcId" --output text 2>/dev/null || true)

if [[ -z "$VPC_ID" || "$VPC_ID" == "None" ]]; then
    echo "[WARN] No default VPC found. Querying available VPCs..."
    VPC_ID=$(aws ec2 describe-vpcs --region "$REGION" --query "Vpcs[0].VpcId" --output text)
fi

echo "[INFO] Using VPC: $VPC_ID"

SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" "Name=map-public-ip-on-launch,Values=true" --region "$REGION" --query "Subnets[0].SubnetId" --output text 2>/dev/null || true)

if [[ -z "$SUBNET_ID" || "$SUBNET_ID" == "None" ]]; then
    SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --region "$REGION" --query "Subnets[0].SubnetId" --output text)
fi

echo "[INFO] Using Subnet: $SUBNET_ID"

# 3. Deploy CloudFormation Stack
echo "[STEP 3/6] Deploying CloudFormation infrastructure stack (Free Tier EC2, EBS, Security Group, IAM, CloudWatch)..."
aws cloudformation deploy \
    --template-file "$PROJECT_ROOT/deploy/cloudformation.yaml" \
    --stack-name "$STACK_NAME" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        VpcId="$VPC_ID" \
        SubnetId="$SUBNET_ID" \
        InstanceType="t3.micro" \
    --region "$REGION"

# 4. Fetch Provisioned Resource Outputs
echo "[STEP 4/6] Fetching stack outputs..."
INSTANCE_ID=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$REGION" --query "Stacks[0].Outputs[?OutputKey=='InstanceId'].OutputValue" --output text)
PUBLIC_IP=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$REGION" --query "Stacks[0].Outputs[?OutputKey=='PublicIp'].OutputValue" --output text)
DASHBOARD_URL="https://$PUBLIC_IP/dashboard"
WEBHOOK_URL="https://$PUBLIC_IP/webhook"

echo "[SUCCESS] EC2 Instance Provisioned: $INSTANCE_ID"
echo "[SUCCESS] Public IPv4 Address: $PUBLIC_IP"
echo "[SUCCESS] Direct HTTPS URL: $DASHBOARD_URL"
echo "[SUCCESS] Webhook URL: $WEBHOOK_URL"

# 5. Instructions for Application Sync & Setup
IP_DASH=${PUBLIC_IP//./-}
SSLIP_DOMAIN="${IP_DASH}.sslip.io"

echo ""
echo "=========================================================="
echo " [STEP 5/6] Deploying Application Code to EC2"
echo "=========================================================="
echo "Browser-Trusted Domain: https://${SSLIP_DOMAIN}/dashboard"
echo ""
echo "To connect to your instance via AWS SSM Session Manager (zero open SSH ports):"
echo "  aws ssm start-session --target $INSTANCE_ID --region $REGION"
echo ""
echo "Inside the instance, clone and start the stack:"
echo "  sudo git clone -b aws-deployment-da3 <YOUR_GIT_REPO_URL> /opt/delta-bot"
echo "  cd /opt/delta-bot"
echo "  sudo bash deploy/setup_ec2.sh"
echo "=========================================================="
echo ""
echo "[STEP 6/6] Verifying CloudWatch log group..."
aws logs describe-log-groups --log-group-name-prefix "/aws/ec2/delta-bot" --region "$REGION" --query "logGroups[0].logGroupName" --output text || true

echo ""
echo "Deployment successfully initialized in $REGION!"
