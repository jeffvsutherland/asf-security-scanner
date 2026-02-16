#!/bin/bash
# ASF Complete Demo - Shows full security lifecycle

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BLUE}${BOLD}============================================================${NC}"
echo -e "${BLUE}${BOLD}🛡️  ASF Security Scanner - Complete Lifecycle Demo${NC}"
echo -e "${BLUE}${BOLD}============================================================${NC}"
echo ""

# Function to pause
pause() {
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read -r
}

# Introduction
echo -e "${BOLD}This demo shows how ASF prevents vulnerabilities like those"
echo -e "that exposed 1.5M tokens in the Moltbook breach.${NC}"
echo ""
echo "We'll examine two real vulnerable skills:"
echo "• oracle - Reads API keys from environment"
echo "• openai-image-gen - Exposes credentials on line 176"
pause

# Step 1: Scan vulnerable skills
echo -e "\n${RED}${BOLD}📍 STEP 1: Scanning Current Skills${NC}"
echo -e "${RED}Running ASF scanner to detect vulnerabilities...${NC}\n"
sleep 1

python3 step1-scan-vulnerable.py
pause

# Step 2: Show the fix
echo -e "\n${GREEN}${BOLD}📍 STEP 2: Creating Secure Versions${NC}"
echo -e "${GREEN}Let's see how we fix these vulnerabilities...${NC}\n"
sleep 1

python3 step2-show-secure-code.py
pause

# Step 3: Verify secure
echo -e "\n${GREEN}${BOLD}📍 STEP 3: Verifying Skills Are Secure${NC}"
echo -e "${GREEN}Running scanner on secure versions...${NC}\n"
sleep 1

python3 step3-verify-secure.py
echo ""

# Summary
echo -e "${BLUE}${BOLD}============================================================${NC}"
echo -e "${BLUE}${BOLD}🏆 Demo Complete!${NC}"
echo -e "${BLUE}${BOLD}============================================================${NC}"
echo ""
echo -e "${BOLD}Key Results:${NC}"
echo -e "• ${RED}BEFORE${NC}: 2 skills with credential exposure vulnerabilities"
echo -e "• ${GREEN}AFTER${NC}: Both skills secured with encrypted credential storage"
echo ""
echo -e "${BOLD}This is how ASF prevents breaches:${NC}"
echo "1. 🔍 Automatically detect vulnerabilities"
echo "2. 🔧 Provide secure implementations"
echo "3. ✅ Verify the fix works"
echo ""
echo -e "${BLUE}Learn more: https://github.com/jeffvsutherland/asf-security-scanner${NC}"
echo ""