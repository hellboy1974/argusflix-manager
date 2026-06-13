#!/bin/bash
# install_ubuntu.sh - Automated installer for ArgusFlix Manager on Ubuntu/Debian

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting ArgusFlix Manager Installation...${NC}"

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root or with sudo.${NC}"
  exit 1
fi

check_and_set_static_ip() {
    echo -e "${YELLOW}Checking network configuration...${NC}"
    
    # Identify default interface
    INTERFACE=$(ip route | awk '/default/ {print $5}' | head -n 1)
    if [ -z "$INTERFACE" ]; then
        echo -e "${RED}Could not find default network interface.${NC}"
        return
    fi

    # Check if DHCP is active (looking at netplan for Ubuntu >= 18.04)
    if grep -E -qR "dhcp4:\s*(true|yes)" /etc/netplan/ 2>/dev/null; then
        CURRENT_IP=$(ip -4 addr show dev $INTERFACE | awk '/inet / {print $2}')
        echo -e "${YELLOW}Current IP address is $CURRENT_IP (DHCP).${NC}"
        read -p "Do you want to change this to a static/fixed IP? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Enter static IP with subnet mask (e.g., 192.168.1.50/24): " STATIC_IP
            read -p "Enter Gateway IP (e.g., 192.168.1.1): " GATEWAY
            read -p "Enter DNS Server (e.g., 8.8.8.8): " DNS_SERVERS

            NETPLAN_FILE=$(ls /etc/netplan/*.yaml | head -n 1)
            if [ -n "$NETPLAN_FILE" ]; then
                # Backup existing configuration
                cp "$NETPLAN_FILE" "${NETPLAN_FILE}.bak"
                
                # Write new configuration
                cat > "$NETPLAN_FILE" <<EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    $INTERFACE:
      dhcp4: no
      addresses:
        - $STATIC_IP
      routes:
        - to: default
          via: $GATEWAY
      nameservers:
        addresses: [$DNS_SERVERS]
EOF
                echo -e "${YELLOW}Applying new network settings via netplan...${NC}"
                netplan apply
                echo -e "${GREEN}Static IP configured successfully.${NC}"
                sleep 2
            else
                echo -e "${RED}No netplan configuration found. Cannot set static IP automatically.${NC}"
            fi
        fi
    else
        CURRENT_IP=$(ip -4 addr show dev $INTERFACE | awk '/inet / {print $2}')
        echo -e "${GREEN}Network is not using DHCP or using an unsupported manager. Current IP: $CURRENT_IP${NC}"
    fi
}

# Run the IP check
check_and_set_static_ip

# 1. System Updates and Dependencies
echo -e "${YELLOW}Updating system packages...${NC}"
apt-get update
apt-get install -y curl wget git jq openssl ca-certificates gnupg lsb-release

# 2. Install Docker & Docker Compose (if not installed)
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    echo -e "${GREEN}Docker is already installed.${NC}"
fi

if ! docker compose version &> /dev/null; then
    echo -e "${YELLOW}Installing Docker Compose plugin...${NC}"
    apt-get install -y docker-compose-plugin
fi

# 3. Clone Repository
REPO_URL="https://github.com/hellboy1974/argusflix-manager.git"
INSTALL_DIR="/opt/argusflix-manager"

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Directory $INSTALL_DIR already exists. Pulling latest changes...${NC}"
    cd $INSTALL_DIR
    git pull
else
    echo -e "${YELLOW}Cloning repository to $INSTALL_DIR...${NC}"
    git clone $REPO_URL $INSTALL_DIR
    cd $INSTALL_DIR
fi

# 4. Prompt for Port Configuration
read -p "Which port should ArgusFlix Manager use? [Default: 8000]: " APP_PORT
APP_PORT=${APP_PORT:-8000}

# 5. Generate .env file
ENV_FILE="$INSTALL_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}Generating .env file with secure defaults...${NC}"
    SECRET_KEY=$(openssl rand -hex 32)
    POSTGRES_PASSWORD=$(openssl rand -hex 16)
    REDIS_PASSWORD=$(openssl rand -hex 16)
    
    cat <<EOF > $ENV_FILE
DEBUG=False
SECRET_KEY=$SECRET_KEY
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Database Settings
POSTGRES_DB=argusflix
POSTGRES_USER=argusflix
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis Settings
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=$REDIS_PASSWORD

# ArgusFlix Settings
API_BASE_URL=http://localhost:$APP_PORT
APP_PORT=$APP_PORT
MEDIA_URL=/media/
STATIC_URL=/static/
EOF
    echo -e "${GREEN}Created .env file.${NC}"
else
    echo -e "${GREEN}.env file already exists. Skipping generation.${NC}"
fi

# 5. Start Docker Containers
echo -e "${YELLOW}Starting Docker containers...${NC}"
# Use the AIO docker-compose file
COMPOSE_CMD="docker compose -f docker/docker-compose.aio.yml"

$COMPOSE_CMD up -d --build

# Wait for database to be ready
echo -e "${YELLOW}Waiting for application to initialize (15 seconds)...${NC}"
sleep 15

# 6. Run Migrations and Load Fixtures
echo -e "${YELLOW}Applying database migrations...${NC}"
$COMPOSE_CMD exec -T argusflix_manager python manage.py migrate

if [ -f "fixtures.json" ]; then
    echo -e "${YELLOW}Loading EPG Pre-Seeding and default fixtures...${NC}"
    $COMPOSE_CMD exec -T argusflix_manager python manage.py loaddata fixtures.json
fi

echo -e "${YELLOW}Collecting static files...${NC}"
$COMPOSE_CMD exec -T argusflix_manager python manage.py collectstatic --noinput

echo -e "${GREEN}================================================================${NC}"
echo -e "${GREEN}ArgusFlix Manager installation complete!${NC}"
echo -e "${GREEN}The Manager should now be accessible at http://<your-server-ip>:$APP_PORT${NC}"
echo -e "${GREEN}================================================================${NC}"
