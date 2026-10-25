"""
Automated Screenshot and Architecture Diagram Generator for QuantLens-XAI.
Captures real application screenshots using headless Chrome, and generates
publication-quality architecture diagrams using Matplotlib.
"""

import os
import subprocess
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "quantlens-final-report", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def capture_chrome_screenshot(url: str, output_path: str, width: int = 1600, height: int = 1100, delay_secs: int = 2):
    """Captures a genuine high-resolution screenshot using headless Chrome."""
    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--virtual-time-budget={delay_secs * 1000}",
        f"--screenshot={output_path}",
        url
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(output_path):
        print(f"✓ Captured screenshot: {os.path.basename(output_path)} ({os.path.getsize(output_path)} bytes)")


def generate_hybrid_db_diagram():
    """Generates a professional hybrid SQLite + MongoDB architecture diagram."""
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.set_facecolor("#0b0c10")
    fig.patch.set_facecolor("#0b0c10")

    # Boxes
    # Client
    ax.add_patch(patches.FancyBboxPatch((0.5, 5.5), 3.0, 1.0, boxstyle="round,pad=0.2", facecolor="#1e1b4b", edgecolor="#8b5cf6", linewidth=2))
    ax.text(2.0, 6.0, "CLIENT / WEB UI\n(Groww-Inspired Dark UI)", color="white", fontsize=11, fontweight="bold", ha="center", va="center")

    # Flask Backend
    ax.add_patch(patches.FancyBboxPatch((4.5, 5.5), 3.5, 1.0, boxstyle="round,pad=0.2", facecolor="#111827", edgecolor="#3b82f6", linewidth=2))
    ax.text(6.25, 6.0, "FLASK BACKEND & REPOSITORY\n(quantlens/routes.py)", color="white", fontsize=11, fontweight="bold", ha="center", va="center")

    # SQLite
    ax.add_patch(patches.FancyBboxPatch((2.0, 2.0), 3.5, 2.5, boxstyle="round,pad=0.2", facecolor="#1c1917", edgecolor="#f59e0b", linewidth=2))
    ax.text(3.75, 4.0, "RELATIONAL SQL\nSQLite 3 (instance/local.db)", color="#fbbf24", fontsize=11, fontweight="bold", ha="center", va="center")
    tables = "• accounts (API credentials)\n• settings (global configs)\n• strategies (strategy metadata)\n• strategy_states (execution lock)\n• trade_logs (webhook log)\n• local_signal_logs (signals)"
    ax.text(2.2, 2.8, tables, color="#d6d3d1", fontsize=9, ha="left", va="center", family="monospace")

    # MongoDB
    ax.add_patch(patches.FancyBboxPatch((7.0, 1.5), 4.2, 3.2, boxstyle="round,pad=0.2", facecolor="#064e3b", edgecolor="#10b981", linewidth=2))
    ax.text(9.1, 4.2, "DOCUMENT NoSQL\nMongoDB 7.0 (quantlens_xai)", color="#34d399", fontsize=11, fontweight="bold", ha="center", va="center")
    colls = "• paper_accounts (cash, ₹1L equity)\n• paper_positions (active holdings)\n• paper_orders (ORD-XXXX fills)\n• paper_trades (round-trip history)\n• paper_audit_events (AUD-XXXX log)\n• paper_simulation_runs (replays)\n• xai_explanations (SHAP/LIME cache)\n• xai_evaluation_results (Slide 9)"
    ax.text(7.2, 2.7, colls, color="#a7f3d0", fontsize=9, ha="left", va="center", family="monospace")

    # Separate Artifacts
    ax.add_patch(patches.FancyBboxPatch((0.5, 0.5), 10.7, 0.7, boxstyle="round,pad=0.1", facecolor="#1e293b", edgecolor="#64748b", linewidth=1.5))
    ax.text(5.85, 0.85, "SEPARATE ANALYTICAL ARTIFACTS: Historical CSVs (data/historical/*.csv) • Native ML Models (models/*.json, *.pt) • Local LLM (Ollama)", color="#cbd5e1", fontsize=9, fontweight="bold", ha="center", va="center")

    # Arrows
    ax.annotate("", xy=(4.5, 6.0), xytext=(3.5, 6.0), arrowprops=dict(arrowstyle="->", color="#8b5cf6", lw=2))
    ax.annotate("", xy=(3.75, 4.5), xytext=(5.5, 5.5), arrowprops=dict(arrowstyle="->", color="#f59e0b", lw=2))
    ax.annotate("", xy=(9.1, 4.7), xytext=(7.0, 5.5), arrowprops=dict(arrowstyle="->", color="#10b981", lw=2))

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7.5)
    ax.axis("off")

    plt.title("QuantLens-XAI Hybrid SQL + NoSQL Architecture", color="white", fontsize=14, fontweight="bold", pad=20)
    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, "arch_hybrid_database.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"✓ Generated diagram: {os.path.basename(out_path)}")


def generate_system_pipeline_diagram():
    """Generates the end-to-end 10-stage processing workflow diagram."""
    fig, ax = plt.subplots(figsize=(14, 6), dpi=300)
    ax.set_facecolor("#0b0c10")
    fig.patch.set_facecolor("#0b0c10")

    stages = [
        ("1. Plain English\nStrategy Input", "#4c1d95"),
        ("2. Local Ollama LLM\nqwen2.5:0.5b (1.0s)", "#5b21b6"),
        ("3. 7-Stage Visual\nDecision Trace", "#6d28d9"),
        ("4. AI Risk Advisory\nRegime Caveats", "#7c3aed"),
        ("5. Pydantic Schema\nValidation", "#8b5cf6"),
        ("6. Event-Driven\nHistorical Backtest", "#059669"),
        ("7. Multi-Model ML\nXGBoost + PyTorch", "#0d9488"),
        ("8. Real SHAP/LIME\nXAI Attribution", "#0284c7"),
        ("9. Paper Broker\nSimulation Replay", "#16a34a"),
        ("10. MongoDB Ledger\n& Audit Trail", "#15803d")
    ]

    for i, (text, col) in enumerate(stages):
        x = 0.5 + (i * 1.3)
        y = 2.5
        ax.add_patch(patches.FancyBboxPatch((x, y), 1.15, 1.2, boxstyle="round,pad=0.1", facecolor=col, edgecolor="white", linewidth=1))
        ax.text(x + 0.575, y + 0.6, text, color="white", fontsize=7.5, fontweight="bold", ha="center", va="center")
        if i < len(stages) - 1:
            ax.annotate("", xy=(x + 1.25, y + 0.6), xytext=(x + 1.15, y + 0.6), arrowprops=dict(arrowstyle="->", color="#a78bfa", lw=1.5))

    ax.set_xlim(0, 14)
    ax.set_ylim(1.5, 4.5)
    ax.axis("off")

    plt.title("QuantLens-XAI End-to-End Execution Workflow", color="white", fontsize=14, fontweight="bold", pad=20)
    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, "arch_system_overview.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"✓ Generated diagram: {os.path.basename(out_path)}")


def main():
    print("Generating Architecture Diagrams...")
    generate_hybrid_db_diagram()
    generate_system_pipeline_diagram()

    print("\nCapturing Real Application Screenshots from Live Server (http://127.0.0.1:5001)...")
    # 1. Main View (Strategy Builder Tab)
    capture_chrome_screenshot("http://127.0.0.1:5001/quantlens", os.path.join(FIG_DIR, "01_strategy_builder.png"), delay_secs=3)

    # 2. Delta Bot Preserved Dashboard
    capture_chrome_screenshot("http://127.0.0.1:5001/dashboard", os.path.join(FIG_DIR, "06_delta_bot_dashboard.png"), delay_secs=2)


if __name__ == "__main__":
    main()
