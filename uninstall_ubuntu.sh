#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting ArgusFlix Manager Uninstallation...${NC}"

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root or with sudo.${NC}"
  exit 1
fi

INSTALL_DIR="/opt/argusflix-manager"

# 1. Stop and remove Docker containers, networks, volumes, and local images
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Stopping and removing Docker resources...${NC}"
    cd "$INSTALL_DIR"
    
    COMPOSE_FILE="ArgusFlix-Manager/docker/docker-compose.aio.yml"
    if [ -f "$COMPOSE_FILE" ]; then
        echo -e "${YELLOW}Running docker compose down to clean up containers, volumes, and images...${NC}"
        docker compose -f "$COMPOSE_FILE" down -v --rmi local || echo -e "${RED}Failed to run docker compose down, continuing cleanup...${NC}"
    else
        echo -e "${YELLOW}Docker compose file not found. Trying to stop containers manually...${NC}"
        docker stop argusflix_manager 2>/dev/null || true
        docker rm -f argusflix_manager 2>/dev/null || true
    fi
else
    echo -e "${YELLOW}Installation directory $INSTALL_DIR not found. Skipping Docker cleanup.${NC}"
fi

# 2. Remove installation files
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Removing installation directory $INSTALL_DIR...${NC}"
    rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}Files removed.${NC}"
else
    echo -e "${YELLOW}Files already removed.${NC}"
fi

echo -e "${GREEN}================================================================${NC}"
echo -e "${GREEN}ArgusFlix Manager has been successfully uninstalled!${NC}"
echo -e "${GREEN}================================================================${NC}"
