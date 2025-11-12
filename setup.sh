#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== Secure LLM Inference Service Setup ===${NC}\n"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}Ollama not found. Installing Ollama...${NC}"
    curl -fsSL https://ollama.ai/install.sh | sh
else
    echo -e "${GREEN}Ollama is already installed${NC}"
fi

# Start Ollama service
echo -e "\n${YELLOW}Starting Ollama service...${NC}"
ollama serve &
sleep 5

# Pull Gemma model
echo -e "\n${YELLOW}Pulling Gemma 2B model (this may take a few minutes)...${NC}"
ollama pull gemma:2b

# Create virtual environment
echo -e "\n${YELLOW}Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "\n${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo -e "\n${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}Please update .env with your configuration${NC}"
fi

echo -e "\n${GREEN}=== Setup Complete ===${NC}"
echo -e "\nTo start the server:"
echo -e "  source venv/bin/activate"
echo -e "  uvicorn app.main:app --reload"
echo -e "\nDefault credentials:"
echo -e "  Username: demo"
echo -e "  Password: demo1234"
