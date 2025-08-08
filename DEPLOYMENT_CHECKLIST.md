# Deployment Checklist for Render

## Pre-Deployment Checklist

### ✅ Code Preparation
- [ ] All code is committed to git repository
- [ ] `render.yaml` file is present and correctly configured
- [ ] `requirements.txt` contains all necessary dependencies
- [ ] `src/main.py` exists and is properly configured
- [ ] Environment variables are documented

### ✅ Repository Setup
- [ ] Repository is pushed to GitHub/GitLab/Bitbucket
- [ ] Repository is public or Render has access
- [ ] Main branch contains the latest code

### ✅ Environment Variables
Make sure you have the following environment variables ready:

#### Required Variables
- [ ] `OPENAI_API_KEY` - Your OpenAI API key
- [ ] `PINECONE_API_KEY` - Your Pinecone API key (optional)
- [ ] `PINECONE_ENVIRONMENT` - Your Pinecone environment (optional)

#### Optional Variables (have defaults)
- [ ] `OPENAI_MODEL` - Default: gpt-4
- [ ] `VECTOR_DB_TYPE` - Default: pinecone
- [ ] `EMBEDDING_MODEL` - Default: text-embedding-ada-002
- [ ] `CHUNK_SIZE` - Default: 1000
- [ ] `CHUNK_OVERLAP` - Default: 200

## Deployment Steps

### Step 1: Render Blueprint Deployment
1. [ ] Go to [Render Dashboard](https://render.com)
2. [ ] Click "New +" → "Blueprint"
3. [ ] Connect your repository
4. [ ] Render will auto-detect `render.yaml`
5. [ ] Enter required environment variables when prompted
6. [ ] Click "Apply" to start deployment

### Step 2: Monitor Deployment
1. [ ] Watch the build logs for any errors
2. [ ] Check that all services are created:
   - [ ] Web service (query-retrieval-api)
   - [ ] PostgreSQL database (query-retrieval-db)
3. [ ] Verify environment variables are set correctly

### Step 3: Test Deployment
1. [ ] Wait for deployment to complete
2. [ ] Test health check endpoint: `GET /api/v1/health`
3. [ ] Test root endpoint: `GET /api/v1/`
4. [ ] Test hackrx test endpoint: `GET /api/v1/hackrx/test`
5. [ ] Test main query endpoint: `POST /api/v1/hackrx/run`

## Post-Deployment Verification

### ✅ Health Checks
- [ ] Health endpoint returns 200 OK
- [ ] Root endpoint returns service information
- [ ] Test endpoint shows configuration details

### ✅ Authentication
- [ ] Valid token returns 200 OK
- [ ] Invalid token returns 401 Unauthorized

### ✅ Main Functionality
- [ ] Can process document URLs
- [ ] Can answer questions about documents
- [ ] Returns structured JSON responses

### ✅ API Documentation
- [ ] Swagger UI accessible at `/api/v1/docs`
- [ ] ReDoc accessible at `/api/v1/redoc`

## Troubleshooting Common Issues

### Build Failures
- [ ] Check `requirements.txt` for missing dependencies
- [ ] Verify Python version compatibility
- [ ] Check for syntax errors in code

### Runtime Errors
- [ ] Check environment variables are set correctly
- [ ] Verify API keys are valid
- [ ] Check logs for specific error messages

### Connection Issues
- [ ] Verify database connection string
- [ ] Check Pinecone configuration
- [ ] Test OpenAI API connectivity

## Performance Monitoring

### ✅ Response Times
- [ ] Health check < 1 second
- [ ] Test endpoint < 2 seconds
- [ ] Query processing < 30 seconds

### ✅ Error Rates
- [ ] < 5% error rate
- [ ] No critical errors in logs
- [ ] Graceful fallbacks working

## Security Verification

### ✅ Authentication
- [ ] API token authentication working
- [ ] Invalid tokens rejected
- [ ] No sensitive data in logs

### ✅ Input Validation
- [ ] URL validation working
- [ ] Question validation working
- [ ] Malicious input handled gracefully

## Final Checklist

### ✅ Documentation
- [ ] API documentation accessible
- [ ] README updated with deployment info
- [ ] Troubleshooting guide available

### ✅ Monitoring
- [ ] Health checks configured
- [ ] Error logging working
- [ ] Performance metrics available

### ✅ Backup
- [ ] Database backup configured
- [ ] Environment variables documented
- [ ] Deployment configuration saved

## Success Criteria

Your deployment is successful when:
- [ ] All health checks pass
- [ ] Authentication works correctly
- [ ] Main query endpoint processes requests
- [ ] API documentation is accessible
- [ ] No critical errors in logs
- [ ] Response times are acceptable

## Support Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)

---

**Note**: This checklist should be completed for each deployment to ensure reliability and performance. 