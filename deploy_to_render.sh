#!/bin/bash

# Deploy to Render - LLM-Powered Intelligent Query-Retrieval System
# This script helps deploy the application to Render using Blueprint

set -e

echo "🚀 Starting deployment to Render..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if we have a remote repository
if ! git remote get-url origin &> /dev/null; then
    echo "❌ No remote repository found. Please add a remote:"
    echo "   git remote add origin <your-repository-url>"
    exit 1
fi

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml not found. Please ensure it exists in the root directory."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please ensure it exists in the root directory."
    exit 1
fi

# Check if main.py exists
if [ ! -f "src/main.py" ]; then
    echo "❌ src/main.py not found. Please ensure it exists."
    exit 1
fi

echo "✅ All prerequisites are met!"

# Push to remote repository
echo "📤 Pushing to remote repository..."
git add .
git commit -m "Deploy to Render - $(date)"
git push origin main

echo ""
echo "🎉 Code pushed successfully!"
echo ""
echo "📋 Next steps for Render deployment:"
echo ""
echo "1. Go to https://render.com and sign in"
echo "2. Click 'New +' and select 'Blueprint'"
echo "3. Connect your repository"
echo "4. Render will automatically detect the render.yaml file"
echo "5. You'll be prompted to enter environment variables:"
echo ""
echo "   Required environment variables (set sync: false):"
echo "   - OPENAI_API_KEY: Your OpenAI API key"
echo "   - PINECONE_API_KEY: Your Pinecone API key"
echo "   - PINECONE_ENVIRONMENT: Your Pinecone environment"
echo ""
echo "6. Click 'Apply' to start the deployment"
echo ""
echo "🔗 After deployment, your API will be available at:"
echo "   https://your-service-name.onrender.com"
echo ""
echo "📚 API Documentation will be available at:"
echo "   https://your-service-name.onrender.com/api/v1/docs"
echo ""
echo "🧪 Test endpoints:"
echo "   - GET /api/v1/health - Health check"
echo "   - GET /api/v1/hackrx/test - Test endpoint"
echo "   - POST /api/v1/hackrx/run - Main query endpoint"
echo ""
echo "🔑 Authentication:"
echo "   Use the Bearer token: 9834d259844d94cfbab31ff7181aa68a50717db4ea92cd1765fb58aabd68cc23"
echo ""
echo "📝 Sample request:"
echo "   curl -X POST 'https://your-service-name.onrender.com/api/v1/hackrx/run' \\"
echo "     -H 'Authorization: Bearer 9834d259844d94cfbab31ff7181aa68a50717db4ea92cd1765fb58aabd68cc23' \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{"
echo "       \"documents\": \"https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D\","
echo "       \"questions\": [\"What is the grace period for premium payment?\"],"
echo "     }'"
echo ""
echo "✅ Deployment script completed!"