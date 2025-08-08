#!/bin/bash

# Bash script for deploying to Render

# Set text colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
WHITE='\033[1;37m'

# Check if Render CLI is installed
if ! command -v render &> /dev/null; then
    echo -e "${RED}Render CLI is not installed. Please install it first or use the Render web dashboard.${NC}"
    echo -e "${YELLOW}You can deploy manually by following the instructions in RENDER_DEPLOYMENT.md${NC}"
    exit 1
fi

# Prompt for Render service name
read -p "Enter a name for your Render service (e.g., query-retrieval-api): " render_service_name

# Prompt for Render database name
read -p "Enter a name for your Render PostgreSQL database (e.g., query-retrieval-db): " render_db_name

# Prompt for environment variables
echo -e "\n${CYAN}Setting up environment variables...${NC}"

# Function to securely prompt for sensitive information
get_secure_input() {
    prompt="$1"
    unset password
    while IFS= read -p "$prompt" -r -s -n 1 char; do
        if [[ $char == $'\0' ]]; then
            break
        fi
        if [[ $char == $'\177' ]]; then
            if [ -n "$password" ]; then
                password="${password%?}"
                echo -en "\b \b"
            fi
        else
            password+="$char"
            echo -n '*'
        fi
    done
    echo
    echo "$password"
}

# OpenAI API Settings
echo -e "${WHITE}OpenAI API Settings:${NC}"
openai_api_key=$(get_secure_input "Enter your OpenAI API Key: ")
read -p "Enter OpenAI Model (default: gpt-4): " openai_model
openai_model=${openai_model:-gpt-4}

# Pinecone Vector Database Settings
echo -e "\n${WHITE}Pinecone Vector Database Settings:${NC}"
pinecone_api_key=$(get_secure_input "Enter your Pinecone API Key: ")
read -p "Enter Pinecone Environment: " pinecone_environment
read -p "Enter Pinecone Index Name: " pinecone_index_name

# API Token for Authentication
echo -e "\n${WHITE}API Authentication:${NC}"
api_token=$(get_secure_input "Enter a secure API Token for authentication: ")

# Document Processing Settings
echo -e "\n${WHITE}Document Processing Settings:${NC}"
read -p "Enter Vector DB Type (pinecone or faiss, default: pinecone): " vector_db_type
vector_db_type=${vector_db_type:-pinecone}

read -p "Enter Embedding Model (default: text-embedding-ada-002): " embedding_model
embedding_model=${embedding_model:-text-embedding-ada-002}

read -p "Enter Embedding Dimension (default: 1536): " embedding_dimension
embedding_dimension=${embedding_dimension:-1536}

read -p "Enter Chunk Size (default: 1000): " chunk_size
chunk_size=${chunk_size:-1000}

read -p "Enter Chunk Overlap (default: 200): " chunk_overlap
chunk_overlap=${chunk_overlap:-200}

echo -e "\n${YELLOW}Note: This script provides guidance for deployment, but you'll need to use the Render web dashboard to complete the process.${NC}"
echo -e "${YELLOW}You can also use the Blueprint deployment option with the render.yaml file in the repository for a more automated setup.${NC}"
echo -e "${CYAN}Please follow these steps:${NC}"

# Create temp_files directory if it doesn't exist
echo -e "\n${GREEN}Creating temp_files directory...${NC}"
mkdir -p temp_files

echo -e "\n${GREEN}1. Log in to your Render dashboard at https://dashboard.render.com${NC}"
echo -e "${GREEN}2. Create a PostgreSQL database named '$render_db_name'${NC}"
echo -e "${GREEN}3. Create a Web Service named '$render_service_name' connected to your repository${NC}"
echo -e "${GREEN}4. Use the following settings for your web service:${NC}"
echo -e "   ${WHITE}- Build Command: pip install -r requirements.txt${NC}"
echo -e "   ${WHITE}- Start Command: uvicorn src.main:app --host 0.0.0.0 --port \$PORT${NC}"

echo -e "\n${GREEN}5. Add the following environment variables to your web service:${NC}"
echo -e "   ${WHITE}OPENAI_API_KEY=$openai_api_key${NC}"
echo -e "   ${WHITE}OPENAI_MODEL=$openai_model${NC}"
echo -e "   ${WHITE}PINECONE_API_KEY=$pinecone_api_key${NC}"
echo -e "   ${WHITE}PINECONE_ENVIRONMENT=$pinecone_environment${NC}"
echo -e "   ${WHITE}PINECONE_INDEX_NAME=$pinecone_index_name${NC}"
echo -e "   ${WHITE}DATABASE_URL=[Use the Internal Database URL from your Render PostgreSQL instance]${NC}"
echo -e "   ${WHITE}HOST=0.0.0.0${NC}"
echo -e "   ${WHITE}PORT=10000${NC}"
echo -e "   ${WHITE}DEBUG_MODE=false${NC}"
echo -e "   ${WHITE}WORKERS=1${NC}"
echo -e "   ${WHITE}API_TOKEN=$api_token${NC}"
echo -e "   ${WHITE}VECTOR_DB_TYPE=$vector_db_type${NC}"
echo -e "   ${WHITE}EMBEDDING_MODEL=$embedding_model${NC}"
echo -e "   ${WHITE}EMBEDDING_DIMENSION=$embedding_dimension${NC}"
echo -e "   ${WHITE}CHUNK_SIZE=$chunk_size${NC}"
echo -e "   ${WHITE}CHUNK_OVERLAP=$chunk_overlap${NC}"
echo -e "   ${WHITE}TEMP_FILES_DIR=temp_files${NC}"

echo -e "\n${GREEN}6. Deploy your application by clicking 'Manual Deploy' and selecting 'Deploy latest commit'${NC}"

echo -e "\n${CYAN}For more detailed instructions, refer to the RENDER_DEPLOYMENT.md file.${NC}"