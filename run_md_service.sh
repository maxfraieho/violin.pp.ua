#!/bin/bash

# ===================================================================
# MD TO EMBEDDINGS SERVICE v4.3 - Simple Reliable Launcher (Linux)
# ===================================================================

set -e  # Exit on any error

# Set UTF-8 encoding
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Script configuration
PYTHON_SCRIPT="md_to_embeddings_service_v4.py"

# Function to print colored output
print_header() {
    echo -e "${BLUE}===================================================================${NC}"
    echo -e "${BLUE}                MD TO EMBEDDINGS SERVICE v4.3${NC}"
    echo -e "${BLUE}===================================================================${NC}"
    echo -e "${YELLOW}Working directory: $(pwd)${NC}"
    echo -e "${BLUE}===================================================================${NC}"
    echo
}

print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_info() {
    echo -e "${YELLOW}$1${NC}"
}

print_cyan() {
    echo -e "${CYAN}$1${NC}"
}

print_magenta() {
    echo -e "${MAGENTA}$1${NC}"
}

# Change to script directory
cd "$(dirname "$0")"

# Clear terminal and show header
clear
print_header

# [1/2] Check Python installation
echo "[1/2] Checking Python..."

if command -v python3 &> /dev/null; then
    print_success "Python3 found"
    python3 --version
    PY_CMD="python3"
elif command -v python &> /dev/null; then
    print_success "Python found"
    python --version
    PY_CMD="python"
else
    echo
    print_error "Python not found!"
    echo
    echo "Please install Python3 using:"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  - CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  - Fedora: sudo dnf install python3 python3-pip"
    echo "  - Arch: sudo pacman -S python python-pip"
    echo
    exit 1
fi

print_success "Python check completed successfully"
echo

# [2/2] Check main script exists
echo "[2/2] Checking main script..."
if [[ -f "$PYTHON_SCRIPT" ]]; then
    print_success "Main script found: $PYTHON_SCRIPT"
else
    echo
    print_error "$PYTHON_SCRIPT not found!"
    echo "Please make sure the file exists in the current directory."
    echo
    exit 1
fi
echo

# Launch service
echo -e "${BLUE}===================================================================${NC}"
echo -e "${BLUE}Launching MD to Embeddings Service v4.3...${NC}"
echo -e "${BLUE}===================================================================${NC}"
echo
print_cyan "MENU OPTIONS:"
echo "  1. 🚀 Deploy project template (first run)"
echo "  2. 🔄 Convert DRAKON schemas (.json → .md)"
echo "  3. 📄 Create aggregated file from project code"
echo "       ${CYAN}→ Can specify ANY directory to process (e.g., /root/.claude/skills)${NC}"
echo "       ${MAGENTA}→ Result saved in script directory${NC}"
echo "       ${CYAN}→ Choose format: .md, .txt, or .pdf${NC}"
echo "       ${MAGENTA}→ PDF format perfect for NotebookLM!${NC}"
echo "       ${CYAN}→ Includes hidden FILES (.env, .gitignore, etc.)${NC}"
echo "       ${CYAN}→ Excludes hidden DIRECTORIES (.git, .venv, etc.)${NC}"
echo "  4. 📤 Copy file to Dropbox/other directory"
echo "  5. 🚪 Exit"
echo
print_info "NEW in v4.3:"
echo "  🎯 Specify target directory for processing"
echo "  💾 Results always saved in script directory"
echo "  🔐 Works with protected directories (e.g., /root)"
echo "  📕 PDF generation support for Google NotebookLM"
echo "  🔍 Automatic dependency checking (reportlab)"
echo
print_magenta "Example usage:"
echo "  • Run script from /home/user/scripts"
echo "  • Choose option 3"
echo "  • Specify /root/.claude/skills as target"
echo "  • Result saved to /home/user/scripts/skills.pdf"
echo
echo -e "${BLUE}===================================================================${NC}"
echo

# Execute the Python script
$PY_CMD "$PYTHON_SCRIPT"
EXIT_CODE=$?

echo
echo -e "${BLUE}===================================================================${NC}"
if [[ $EXIT_CODE -eq 0 ]]; then
    print_success "Service completed successfully"
else
    print_error "Service exited with code: $EXIT_CODE"
fi
echo -e "${BLUE}===================================================================${NC}"
echo

# Wait for user input (Linux equivalent of pause)
read -p "Press Enter to continue..." -r
exit $EXIT_CODE