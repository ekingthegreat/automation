"""
scheduler.py
Runs the fruit story pipeline automatically on a schedule.
Uses Python's built-in 'schedule' library — FREE.

Install: pip install schedule
Run: python scheduler.py   (keep this running in background)
"""

import schedule
import time
import logging
from datetime import datetime
from main import run_pipeline

# ── LOGGING SETUP ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot_log.txt"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_with_error_handling():
    """Run pipeline and catch any errors so the scheduler keeps going."""
    try:
        logger.info("🍎 Starting scheduled fruit story generation...")
        run_pipeline()
        logger.info("✅ Pipeline completed successfully!\n")
    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}")
        logger.info("⏩ Will retry at next scheduled time.\n")


# ── SCHEDULE CONFIGURATION ─────────────────────────────────────────────────
# Choose your preferred posting times (24-hour format)
# Best times for Filipino audience: 9AM, 12PM, 7PM, 9PM

# Option A: Post once per day at 9 AM
schedule.every().day.at("09:00").do(run_with_error_handling)

# Option B: Post twice per day (uncomment to use)
# schedule.every().day.at("09:00").do(run_with_error_handling)
# schedule.every().day.at("19:00").do(run_with_error_handling)

# Option C: Post every 6 hours (4x per day) (uncomment to use)
# schedule.every(6).hours.do(run_with_error_handling)

# Option D: Run once immediately for testing (uncomment to use)
# run_with_error_handling()


def main():
    logger.info("="*50)
    logger.info("  🍎 FRUIT STORY BOT SCHEDULER STARTED")
    logger.info(f"  🕐 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("  📅 Scheduled: Daily at 09:00")
    logger.info("  🛑 Press Ctrl+C to stop")
    logger.info("="*50 + "\n")

    while True:
        schedule.run_pending()
        time.sleep(60)   # Check every minute


if __name__ == "__main__":
    main()
