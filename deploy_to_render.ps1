# PowerShell script for deploying to Render

# Check if Render CLI is installed
$renderCliInstalled = $null
try {
    $renderCliInstalled = Get-Command render -ErrorAction SilentlyContinue
} catch {
    # Command not found
}

if (-not $renderCliInstalled) {
    Write-Host "Render CLI is not installed. Please install it first or use the Render web dashboard." -ForegroundColor Red
    Write-Host "You can deploy manually by following the instructions in RENDER_DEPLOYMENT.md" -ForegroundColor Yellow
    exit 1
}

# Prompt for Render service name
$renderServiceName = Read-Host -Prompt "Enter a name for your Render service (e.g., query-retrieval-api)"

# Prompt for Render database name
$renderDbName = Read-Host -Prompt "Enter a name for your Render PostgreSQL database (e.g., query-retrieval-db)"

# Prompt for environment variables
Write-Host "`nSetting up environment variables..." -ForegroundColor Cyan

# Function to securely prompt for sensitive information
function Get-SecureInput {
    param (
        [string]$prompt
    )
    
    $secureString = Read-Host -Prompt $prompt -AsSecureString
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString)
    $plainText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)
    
    return $plainText
}

# OpenAI API Settings
$openaiApiKey = Get-SecureInput "Enter your OpenAI API Key"
$openaiModel = Read-Host -Prompt "Enter OpenAI Model (default: gpt-4)"
if (-not $openaiModel) { $openaiModel = "gpt-4" }

# Pinecone Vector Database Settings
$pineconeApiKey = Get-SecureInput "Enter your Pinecone API Key"
$pineconeEnvironment = Read-Host -Prompt "Enter Pinecone Environment"
$pineconeIndexName = Read-Host -Prompt "Enter Pinecone Index Name"

# API Token for Authentication
$apiToken = Get-SecureInput "Enter a secure API Token for authentication"

# Document Processing Settings
$vectorDbType = Read-Host -Prompt "Enter Vector DB Type (pinecone or faiss, default: pinecone)"
if (-not $vectorDbType) { $vectorDbType = "pinecone" }

$embeddingModel = Read-Host -Prompt "Enter Embedding Model (default: text-embedding-ada-002)"
if (-not $embeddingModel) { $embeddingModel = "text-embedding-ada-002" }

$embeddingDimension = Read-Host -Prompt "Enter Embedding Dimension (default: 1536)"
if (-not $embeddingDimension) { $embeddingDimension = "1536" }

$chunkSize = Read-Host -Prompt "Enter Chunk Size (default: 1000)"
if (-not $chunkSize) { $chunkSize = "1000" }

$chunkOverlap = Read-Host -Prompt "Enter Chunk Overlap (default: 200)"
if (-not $chunkOverlap) { $chunkOverlap = "200" }

Write-Host "`nNote: This script provides guidance for deployment, but you'll need to use the Render web dashboard to complete the process." -ForegroundColor Yellow
Write-Host "You can also use the Blueprint deployment option with the render.yaml file in the repository for a more automated setup." -ForegroundColor Yellow

# Create temp_files directory if it doesn't exist
Write-Host "`nCreating temp_files directory..." -ForegroundColor Green
if (-not (Test-Path -Path "temp_files")) {
    New-Item -ItemType Directory -Path "temp_files" | Out-Null
}

Write-Host "Please follow these steps:" -ForegroundColor Cyan

Write-Host "`n1. Log in to your Render dashboard at https://dashboard.render.com" -ForegroundColor Green
Write-Host "2. Create a PostgreSQL database named '$renderDbName'" -ForegroundColor Green
Write-Host "3. Create a Web Service named '$renderServiceName' connected to your repository" -ForegroundColor Green
Write-Host "4. Use the following settings for your web service:" -ForegroundColor Green
Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor White
Write-Host "   - Start Command: uvicorn src.main:app --host 0.0.0.0 --port `$PORT" -ForegroundColor White

Write-Host "`n5. Add the following environment variables to your web service:" -ForegroundColor Green
Write-Host "   OPENAI_API_KEY=$openaiApiKey" -ForegroundColor White
Write-Host "   OPENAI_MODEL=$openaiModel" -ForegroundColor White
Write-Host "   PINECONE_API_KEY=$pineconeApiKey" -ForegroundColor White
Write-Host "   PINECONE_ENVIRONMENT=$pineconeEnvironment" -ForegroundColor White
Write-Host "   PINECONE_INDEX_NAME=$pineconeIndexName" -ForegroundColor White
Write-Host "   DATABASE_URL=[Use the Internal Database URL from your Render PostgreSQL instance]" -ForegroundColor White
Write-Host "   HOST=0.0.0.0" -ForegroundColor White
Write-Host "   PORT=10000" -ForegroundColor White
Write-Host "   DEBUG_MODE=false" -ForegroundColor White
Write-Host "   WORKERS=1" -ForegroundColor White
Write-Host "   API_TOKEN=$apiToken" -ForegroundColor White
Write-Host "   VECTOR_DB_TYPE=$vectorDbType" -ForegroundColor White
Write-Host "   EMBEDDING_MODEL=$embeddingModel" -ForegroundColor White
Write-Host "   EMBEDDING_DIMENSION=$embeddingDimension" -ForegroundColor White
Write-Host "   CHUNK_SIZE=$chunkSize" -ForegroundColor White
Write-Host "   CHUNK_OVERLAP=$chunkOverlap" -ForegroundColor White
Write-Host "   TEMP_FILES_DIR=temp_files" -ForegroundColor White

Write-Host "`n6. Deploy your application by clicking 'Manual Deploy' and selecting 'Deploy latest commit'" -ForegroundColor Green

Write-Host "`nFor more detailed instructions, refer to the RENDER_DEPLOYMENT.md file." -ForegroundColor Cyan