# Deploying to Render

This guide provides step-by-step instructions for deploying the LLM-powered intelligent query-retrieval system to Render, a cloud platform that offers a free tier for web services and PostgreSQL databases.

## Prerequisites

1. A [Render account](https://render.com/) (free tier available)
2. Your project code pushed to a GitHub, GitLab, or Bitbucket repository
3. OpenAI API key and other required environment variables

## Deployment Options

There are two ways to deploy this application to Render:

1. **Manual Deployment** - Follow the step-by-step instructions below
2. **Blueprint Deployment** - Use the `render.yaml` file in the repository for a more automated setup

### Blueprint Deployment (Recommended)

1. Fork or clone this repository to your GitHub, GitLab, or Bitbucket account
2. Log in to your Render dashboard
3. Click on "New +" and select "Blueprint"
4. Connect your repository
5. Render will automatically detect the `render.yaml` file and set up the services
6. You'll be prompted to enter values for environment variables marked with `sync: false`
7. Click "Apply" to start the deployment

## Manual Deployment Steps

### Step 1: Set Up PostgreSQL Database on Render

1. Log in to your Render dashboard
2. Click on "New +" and select "PostgreSQL"
3. Configure your database:
   - Name: Choose a name for your database (e.g., `query-retrieval-db`)
   - Database: Choose a database name
   - User: The database user will be created automatically
   - Region: Select a region close to your target users
   - PostgreSQL Version: Select version 14 (to match development environment)
4. Click "Create Database"
5. Once created, note the following information from the database dashboard:
   - Internal Database URL
   - External Database URL
   - Username
   - Password

### Step 2: Deploy Web Service

1. In your Render dashboard, click on "New +" and select "Web Service"
2. Connect your GitHub/GitLab/Bitbucket repository
3. Configure your web service:
   - Name: Choose a name for your service (e.g., `query-retrieval-api`)
   - Region: Select the same region as your database
   - Branch: Select the branch to deploy (usually `main` or `master`)
   - Runtime: Select "Python 3"
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: Select "Free" for testing (upgrade for production)

### Step 3: Configure Environment Variables

1. In your web service dashboard, go to the "Environment" tab
2. Add the following environment variables (based on your `.env.example` file):

```
# OpenAI API Settings
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4

# Pinecone Vector Database Settings
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=your_pinecone_index_name

# Database URL (use the Internal Database URL from Step 1)
DATABASE_URL=your_internal_database_url

# Server Settings
HOST=0.0.0.0
PORT=10000
DEBUG_MODE=false
WORKERS=1

# API Token for Authentication
API_TOKEN=your_secure_api_token

# Document Processing Settings
VECTOR_DB_TYPE=pinecone  # or faiss
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_DIMENSION=1536
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TEMP_FILES_DIR=temp_files
```

3. Click "Save Changes"

### Step 4: Deploy and Monitor

1. Click "Manual Deploy" and select "Deploy latest commit"
2. Monitor the deployment logs for any errors
3. Once deployed, your API will be available at `https://your-service-name.onrender.com`

## Verifying Deployment

1. Access your API documentation at `https://your-service-name.onrender.com/api/v1/docs`
2. Test the API endpoints using the Swagger UI
3. Make a sample request to the `/hackrx/run` endpoint with proper authentication

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Ensure you're using the Internal Database URL for connections from your web service
   - Check that your database is in the same region as your web service

2. **Application Errors**:
   - Check the logs in your Render dashboard for error messages
   - Verify all environment variables are correctly set

3. **Slow Performance**:
   - The free tier has limited resources and may experience cold starts
   - Consider upgrading to a paid plan for production use

### Render-Specific Notes

1. **Free Tier Limitations**:
   - Free web services are automatically spun down after 15 minutes of inactivity
   - They take a few seconds to spin up when a new request comes in
   - PostgreSQL databases on the free tier expire after 90 days

2. **Scaling**:
   - For production use, consider upgrading to a paid plan
   - Render offers automatic scaling options for paid plans

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render PostgreSQL Documentation](https://render.com/docs/databases)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)