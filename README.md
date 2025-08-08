# LLM-Powered Intelligent Query-Retrieval System

A sophisticated document processing and query system that can handle large documents and make contextual decisions for insurance, legal, HR, and compliance domains.

## 🚀 Features

- **Multi-format Document Processing**: Supports PDF, DOCX, and email documents
- **Semantic Search**: Uses FAISS/Pinecone for efficient vector search
- **LLM Integration**: Powered by OpenAI GPT-4 for intelligent query processing
- **Structured Responses**: Returns JSON-formatted answers with explainable reasoning
- **Authentication**: Secure API token-based authentication
- **Scalable Architecture**: Modular design for easy extension

## 🏗️ System Architecture

```
Input Documents → LLM Parser → Embedding Search → Clause Matching → Logic Evaluation → JSON Output
```

### Components

1. **Document Processor**: Extracts text from various document formats
2. **Vector Store**: Manages embeddings using FAISS or Pinecone
3. **Query Processor**: Processes natural language queries
4. **LLM Service**: Handles OpenAI API interactions
5. **API Layer**: FastAPI-based REST API

## 📋 Prerequisites

- Python 3.9+
- OpenAI API key
- Pinecone API key (optional, falls back to FAISS)
- PostgreSQL database (for production)

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd bajaj
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env with your API keys
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   ```

4. **Run the application**
   ```bash
   python src/main.py
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t query-retrieval-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 query-retrieval-api
   ```

## 🌐 Render Deployment

### Option 1: Blueprint Deployment (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Deploy using Render Blueprint**
   - Go to [Render Dashboard](https://render.com)
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will automatically detect `render.yaml`
   - Enter required environment variables:
     - `OPENAI_API_KEY`
     - `PINECONE_API_KEY`
     - `PINECONE_ENVIRONMENT`
   - Click "Apply"

### Option 2: Manual Deployment

1. **Create PostgreSQL Database**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Configure database settings
   - Note the connection string

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   ```
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   DATABASE_URL=your_database_connection_string
   HOST=0.0.0.0
   PORT=10000
   DEBUG_MODE=false
   WORKERS=1
   API_TOKEN=9834d259844d94cfbab31ff7181aa68a50717db4ea92cd1765fb58aabd68cc23
   VECTOR_DB_TYPE=pinecone
   EMBEDDING_MODEL=text-embedding-ada-002
   EMBEDDING_DIMENSION=1536
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   TEMP_FILES_DIR=temp_files
   ```

## 📚 API Documentation

### Base URL
- **Local**: `http://localhost:8000/api/v1`
- **Render**: `https://your-service-name.onrender.com/api/v1`

### Authentication
Use Bearer token: `9834d259844d94cfbab31ff7181aa68a50717db4ea92cd1765fb58aabd68cc23`

### Endpoints

#### Health Check
```bash
GET /api/v1/health
```

#### Test Endpoint
```bash
GET /api/v1/hackrx/test
```

#### Main Query Endpoint
```bash
POST /api/v1/hackrx/run
Content-Type: application/json
Authorization: Bearer 9834d259844d94cfbab31ff7181aa68a50717db4ea92cd1765fb58aabd68cc23

{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?"
    ]
}
```

### Sample Response
```json
{
    "answers": [
        "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.",
        "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered.",
        "Yes, the policy covers maternity expenses, including childbirth and lawful medical termination of pregnancy. To be eligible, the female insured person must have been continuously covered for at least 24 months."
    ]
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` |
| `PINECONE_API_KEY` | Pinecone API key | Optional |
| `PINECONE_ENVIRONMENT` | Pinecone environment | Optional |
| `PINECONE_INDEX_NAME` | Pinecone index name | `document-retrieval` |
| `VECTOR_DB_TYPE` | Vector database type | `pinecone` |
| `EMBEDDING_MODEL` | Embedding model | `text-embedding-ada-002` |
| `CHUNK_SIZE` | Text chunk size | `1000` |
| `CHUNK_OVERLAP` | Chunk overlap | `200` |
| `API_TOKEN` | API authentication token | Default provided |

### Supported Document Types

- PDF files
- DOCX files
- Text files
- Email files (EML)

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Ensure you're running from the project root directory

#### 2. Pinecone Connection Issues
**Problem**: Pinecone initialization fails
**Solution**: The system automatically falls back to FAISS if Pinecone is not configured

#### 3. OpenAI API Errors
**Problem**: `openai.error.AuthenticationError`
**Solution**: Verify your OpenAI API key is correct and has sufficient credits

#### 4. Render Deployment Failures
**Problem**: Build fails on Render
**Solution**: 
- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify environment variables are set correctly

#### 5. Port Issues
**Problem**: Application won't start
**Solution**: 
- Local: Use port 8000
- Render: Use `$PORT` environment variable

### Debug Mode

Enable debug mode for detailed logging:
```bash
export DEBUG_MODE=true
```

## 📊 Performance Optimization

### Token Efficiency
- Uses chunking to process large documents
- Implements retry logic with exponential backoff
- Optimizes embedding generation

### Latency Optimization
- Asynchronous processing
- Background task cleanup
- Efficient vector search

### Scalability
- Modular architecture
- Configurable vector database backends
- Horizontal scaling support

## 🔒 Security

- API token authentication
- Input validation
- Secure environment variable handling
- CORS configuration

## 📈 Monitoring

### Health Checks
- `/api/v1/health` - Basic health check
- `/api/v1/hackrx/test` - Detailed system status

### Logging
- Structured logging with different levels
- Error tracking and reporting
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Check Render deployment logs
4. Open an issue on GitHub

---

**Note**: This system is designed for the HackRx competition and includes specific optimizations for insurance, legal, HR, and compliance document processing.