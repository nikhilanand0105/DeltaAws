#!/usr/bin/env bash
# ==============================================================================
# Single-Command Cleanup Script to Teardown AWS Resources & Prevent Charges
# ==============================================================================
set -euo pipefail

STACK_NAME="delta-trading-bot-stack"
REGION="${AWS_REGION:-${AWS_DEFAULT_REGION:-ap-south-1}}"

echo "=========================================================="
echo " AWS Cloud Architecture Teardown Script"
echo " Target Stack: $STACK_NAME"
echo " Target Region: $REGION"
echo "=========================================================="

read -p "Are you sure you want to permanently delete all AWS resources for $STACK_NAME? (y/N): " -r CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    echo "[CANCELLED] Teardown aborted by user."
    exit 0
fi

echo "[INFO] Initiating CloudFormation stack deletion in $REGION..."
aws cloudformation delete-stack --stack-name "$STACK_NAME" --region "$REGION"

echo "[INFO] Waiting for stack deletion to complete (this terminates the EC2 instance, releases IPv4, and deletes EBS storage)..."
aws cloudformation wait stack-delete-complete --stack-name "$STACK_NAME" --region "$REGION"

echo "[INFO] Cleaning up CloudWatch Log Group..."
aws logs delete-log-group --log-group-name "/aws/ec2/delta-bot" --region "$REGION" 2>/dev/null || true

echo "=========================================================="
echo " [SUCCESS] All AWS resources have been completely deleted!"
echo " Zero ongoing compute, storage, or IP charges will be billed."
echo "=========================================================="
