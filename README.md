# LLM-Powered Intelligent Query-Retrieval System

An intelligent system that can process large documents and make contextual decisions for insurance, legal, HR, and compliance domains.

## Features

- Process PDFs, DOCX, and email documents
- Handle policy/contract data efficiently
- Parse natural language queries
- Use embeddings (FAISS/Pinecone) for semantic search
- Implement clause retrieval and matching
- Provide explainable decision rationale
- Output structured JSON responses

## System Architecture

1. **Input Documents**: PDF Blob URL
2. **LLM Parser**: Extract structured query
3. **Embedding Search**: FAISS/Pinecone retrieval
4. **Clause Matching**: Semantic similarity
5. **Logic Evaluation**: Decision processing
6. **JSON Output**: Structured response

## Tech Stack

- **Backend**: FastAPI
- **Vector DB**: Pinecone/FAISS
- **LLM**: GPT-4
- **Database**: PostgreSQL

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- OpenAI API Key
- Pinecone API Key (optional, can use FAISS locally)

### Installation

1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
PINCONE_API_KEY=your_pinecone_api_key
PINCONE_ENVIRONMENT=your_pinecone_environment
PINCONE_INDEX_NAME=document-retrieval
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/document_retrieval
```

4. Create the temporary files directory

```bash
mkdir -p ./temp_files
```

### Running the Application

```bash
cd src
python main.py
```

The API will be available at `http://localhost:8000/api/v1`

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

### Authentication

All API endpoints require authentication using a Bearer token:

```
Authorization: Bearer 9834d259844d94cfbab31ff7181aa68a50717db4ea92cd1765fb58aabd68cc23
```

### Sample Request

```json
POST /api/v1/hackrx/run
Content-Type: application/json
Accept: application/json
Authorization: Bearer 9834d259844d94cfbab31ff7181aa68a50717db4ea92cd1765fb58aabd68cc23

{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?"
    ]
}
```

### Sample Response

```json
{
    "answers": [
        "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.",
        "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered."
    ]
}
```

## Evaluation Parameters

The system is designed to optimize for:

1. **Accuracy**: Precision of query understanding and clause matching
2. **Token Efficiency**: Optimized LLM token usage and cost-effectiveness
3. **Latency**: Response speed and real-time performance
4. **Reusability**: Code modularity and extensibility
5. **Explainability**: Clear decision reasoning and clause traceability

## Deployment

### Deploying to Render

This project includes scripts and configuration for easy deployment to Render, which offers a free tier for web services and PostgreSQL databases. For detailed instructions, see the [Render Deployment Guide](RENDER_DEPLOYMENT.md).

#### Deployment Options

1. **Blueprint Deployment (Recommended)**
   - Fork/clone this repository to your GitHub/GitLab/Bitbucket account
   - In Render dashboard, select "New +" > "Blueprint"
   - Connect your repository
   - Render will automatically configure services using the `render.yaml` file

2. **Guided Deployment**
   - Run the deployment script:

   ```bash
   # For Windows
   .\deploy_to_render.ps1
   
   # For Unix-based systems
   chmod +x deploy_to_render.sh
   ./deploy_to_render.sh
   ```

   - Follow the prompts and instructions to configure your Render application



## License

This project is licensed under the MIT License - see the LICENSE file for details.