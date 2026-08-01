"""
Main entry point - redirects to CLI menu for two-step workflow.
"""

import sys

# Import and run the CLI
from cli import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n?? Cancelled by user")
        sys.exit(0)

# LEGACY CODE - NO LONGER USED
#
# The original monolithic orchestrator has been replaced with:
# - cli.py: Menu-driven interface for workflow selection
# - steps/step1_scraper_only.py: Scraping only
# - steps/step2_ai_analysis.py: AI content enrichment
#
# See motor/WORKFLOW.py for complete documentation
