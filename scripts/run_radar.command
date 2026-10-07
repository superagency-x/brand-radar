#!/bin/bash
# ==============================================================================
# Brand Radar · German Marketing Intelligence Runner
# ==============================================================================

export PATH="$HOME/.local/bin:$HOME/.cargo/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

PROJECT_DIR="/Users/berksaraloglu/Projects/brand-radar"
cd "$PROJECT_DIR" || exit 1

BOLD=$(tput bold 2>/dev/null || echo "")
NORMAL=$(tput sgr0 2>/dev/null || echo "")
BLUE=$(tput setaf 4 2>/dev/null || echo "")
CYAN=$(tput setaf 6 2>/dev/null || echo "")
GREEN=$(tput setaf 2 2>/dev/null || echo "")
YELLOW=$(tput setaf 3 2>/dev/null || echo "")
DIM=$(tput dim 2>/dev/null || echo "")

clear

echo "${BLUE}╔══════════════════════════════════════════════════════════════════════╗${NORMAL}"
echo "${BLUE}║${NORMAL}                 ${BOLD}${CYAN}B R A N D   R A D A R${NORMAL}                                ${BLUE}║${NORMAL}"
echo "${BLUE}║${NORMAL}       ${DIM}German Marketing Intelligence & Competitive Teardown${NORMAL}           ${BLUE}║${NORMAL}"
echo "${BLUE}╚══════════════════════════════════════════════════════════════════════╝${NORMAL}"
echo ""
echo "${BOLD}Target Market:${NORMAL} Germany (DE)"
echo "${BOLD}Target Brands:${NORMAL} SharkNinja · Cosori · Philips · Tefal"
echo "${BOLD}Intelligence Vectors:${NORMAL}"
echo "  • Meta Ad Library (Facebook & Instagram Active Ads & 1Y Archive)"
echo "  • Google SEM (Paid Ads, Shopping PLAs, Generic Category SERP Ranks)"
echo "  • Affiliate Communities (MyDealz Heat, Voucher Codes, Awin Tracking)"
echo "  • Modeled Media Investments (CPM/CPC Benchmarks & Seasonality Curves)"
echo "  • PR & Editorial Coverage (Presseportal & Stiftung Warentest Awards)"
echo "  • E-Retailer Collaborations (MediaMarkt, Otto, Amazon Brand Stores)"
echo ""
echo "${CYAN}──────────────────────────────────────────────────────────────────────${NORMAL}"
echo "  ${GREEN}[1] Run Live Intelligence Scraper${NORMAL}  (Auto-starts in 4s...)"
echo "      Scrapes updated intelligence across all 6 pillars, computes"
echo "      competitive models, and automatically launches dashboard"
echo ""
echo "  ${YELLOW}[2] Open Interactive Dashboard${NORMAL} (Instant view, no scraping)"
echo "      Launches local server at http://localhost:8080"
echo ""
echo "  ${BLUE}[3] View Executive Dossier${NORMAL} (Printable report & markdown)"
echo "      Opens the generated C-level marketing dossier"
echo "${CYAN}──────────────────────────────────────────────────────────────────────${NORMAL}"
echo ""

CHOICE="1"
if read -t 4 -p "${BOLD}Select option [1-3] or press Enter to scrape:${NORMAL} " USER_INPUT; then
    if [ -n "$USER_INPUT" ]; then
        CHOICE="$USER_INPUT"
    fi
fi
echo ""

UV_BIN=$(which uv 2>/dev/null || echo "$HOME/.local/bin/uv")
if [ ! -x "$UV_BIN" ]; then
    echo "Error: 'uv' package manager not found. Please check your installation."
    read -p "Press Enter to exit..."
    exit 1
fi

case "$CHOICE" in
    1)
        echo "${GREEN}▶ Executing live marketing intelligence retrieval...${NORMAL}"
        echo ""
        "$UV_BIN" run brand-radar run
        EXIT_CODE=$?
        echo ""
        if [ $EXIT_CODE -eq 0 ]; then
            echo "${GREEN}✔ Intelligence pipeline completed successfully!${NORMAL}"
            echo "${CYAN}▶ Launching interactive dashboard at http://localhost:8080 ...${NORMAL}"
            (sleep 1 && open "http://localhost:8080") &
            "$UV_BIN" run brand-radar serve --port 8080
        else
            echo "${YELLOW}Pipeline exited with code $EXIT_CODE.${NORMAL}"
            read -p "Press Enter to close this window..."
        fi
        ;;
    2)
        echo "${CYAN}▶ Launching interactive dashboard at http://localhost:8080 ...${NORMAL}"
        (sleep 1 && open "http://localhost:8080") &
        "$UV_BIN" run brand-radar serve --port 8080
        ;;
    3)
        echo "${BLUE}▶ Opening executive marketing intelligence dossier...${NORMAL}"
        "$UV_BIN" run brand-radar report
        LATEST_HTML=$(ls -t data/exports/marketing_intel_*.html 2>/dev/null | head -1)
        if [ -n "$LATEST_HTML" ]; then
            open "$LATEST_HTML"
        fi
        echo ""
        read -p "Press Enter to close this window..."
        ;;
    *)
        echo "Invalid selection. Exiting."
        sleep 2
        ;;
esac
