import os
import json
import logging
from typing import List, Dict, Any, Optional, Union
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """
    Service for interacting with Language Models (LLMs) for various NLP tasks.
    Supports OpenAI GPT models and can be extended to support other LLMs.
    """
    
    def __init__(self):
        self.llm_type = settings.LLM_TYPE
        self.model = settings.OPENAI_MODEL if self.llm_type == "openai" else None
        self.embedding_model = settings.EMBEDDING_MODEL
        
        logger.info(f"Initialized LLMService with {self.llm_type} backend")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def extract_structured_query(self, query: str) -> str:
        """
        Extract a structured query from a natural language query.
        
        Args:
            query: The natural language query.
            
        Returns:
            str: The structured query.
        """
        try:
            if self.llm_type == "openai":
                return await self._openai_extract_structured_query(query)
            else:
                raise ValueError(f"Unsupported LLM type: {self.llm_type}")
        
        except Exception as e:
            logger.error(f"Error extracting structured query: {str(e)}")
            raise
    
    async def _openai_extract_structured_query(self, query: str) -> str:
        """
        Extract a structured query using OpenAI.
        
        Args:
            query: The natural language query.
            
        Returns:
            str: The structured query.
        """
        try:
            import openai
            openai.api_key = settings.OPENAI_API_KEY
            
            # Define the prompt
            prompt = f"""
            You are an AI assistant that helps extract structured queries from natural language questions.
            Please analyze the following question and extract the key concepts, entities, and relationships.
            Format your response as a concise search query that captures the essence of the question.
            
            Question: {query}
            
            Structured Query:
            """
            
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts structured queries from natural language questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            # Extract the structured query
            structured_query = response.choices[0].message.content.strip()
            
            logger.info(f"Extracted structured query: {structured_query}")
            return structured_query
        
        except Exception as e:
            logger.error(f"Error with OpenAI extraction: {str(e)}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of texts to generate embeddings for.
            
        Returns:
            List[List[float]]: List of embedding vectors.
        """
        try:
            if self.llm_type == "openai":
                return await self._openai_get_embeddings(texts)
            else:
                raise ValueError(f"Unsupported LLM type: {self.llm_type}")
        
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    async def _openai_get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using OpenAI.
        
        Args:
            texts: List of texts to generate embeddings for.
            
        Returns:
            List[List[float]]: List of embedding vectors.
        """
        try:
            import openai
            openai.api_key = settings.OPENAI_API_KEY
            
            # Call OpenAI API
            response = await openai.Embedding.acreate(
                model=self.embedding_model,
                input=texts
            )
            
            # Extract embeddings
            embeddings = [data.embedding for data in response.data]
            
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
        
        except Exception as e:
            logger.error(f"Error with OpenAI embeddings: {str(e)}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_answer(self, query: str, context: List[str], structured_query: Optional[str] = None) -> str:
        """
        Generate an answer to a query based on the provided context.
        
        Args:
            query: The original query.
            context: List of relevant text chunks.
            structured_query: Optional structured query for better context.
            
        Returns:
            str: The generated answer.
        """
        try:
            if self.llm_type == "openai":
                return await self._openai_generate_answer(query, context, structured_query)
            else:
                raise ValueError(f"Unsupported LLM type: {self.llm_type}")
        
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise
    
    async def _openai_generate_answer(self, query: str, context: List[str], structured_query: Optional[str] = None) -> str:
        """
        Generate an answer using OpenAI.
        
        Args:
            query: The original query.
            context: List of relevant text chunks.
            structured_query: Optional structured query for better context.
            
        Returns:
            str: The generated answer.
        """
        try:
            import openai
            openai.api_key = settings.OPENAI_API_KEY
            
            # Combine context chunks
            combined_context = "\n\n---\n\n".join(context)
            
            # Define the prompt
            prompt = f"""
            You are an AI assistant that helps answer questions based on the provided context.
            Please analyze the following question and context, and provide a concise, accurate answer.
            If the answer cannot be found in the context, please state that clearly.
            
            Question: {query}
            
            Context:
            {combined_context}
            
            Answer:
            """
            
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )
            
            # Extract the answer
            answer = response.choices[0].message.content.strip()
            
            logger.info(f"Generated answer: {answer[:50]}...")
            return answer
        
        except Exception as e:
            logger.error(f"Error with OpenAI answer generation: {str(e)}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def evaluate_logic(self, query: str, context: List[str]) -> Dict[str, Any]:
        """
        Evaluate the logic of a query against the provided context.
        
        Args:
            query: The query to evaluate.
            context: List of relevant text chunks.
            
        Returns:
            Dict[str, Any]: The evaluation result.
        """
        try:
            if self.llm_type == "openai":
                return await self._openai_evaluate_logic(query, context)
            else:
                raise ValueError(f"Unsupported LLM type: {self.llm_type}")
        
        except Exception as e:
            logger.error(f"Error evaluating logic: {str(e)}")
            raise
    
    async def _openai_evaluate_logic(self, query: str, context: List[str]) -> Dict[str, Any]:
        """
        Evaluate the logic using OpenAI.
        
        Args:
            query: The query to evaluate.
            context: List of relevant text chunks.
            
        Returns:
            Dict[str, Any]: The evaluation result.
        """
        try:
            import openai
            openai.api_key = settings.OPENAI_API_KEY
            
            # Combine context chunks
            combined_context = "\n\n---\n\n".join(context)
            
            # Define the prompt
            prompt = f"""
            You are an AI assistant that helps evaluate the logic of a query against the provided context.
            Please analyze the following question and context, and provide a structured evaluation.
            
            Question: {query}
            
            Context:
            {combined_context}
            
            Evaluation (in JSON format):
            {{
                "relevant_clauses": ["List of relevant clauses found in the context"],
                "decision": "yes/no/partial",
                "confidence": 0.0 to 1.0,
                "reasoning": "Explanation of the decision",
                "conditions": ["List of conditions if applicable"],
                "references": ["List of specific references to the context"]
            }}
            """
            
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that evaluates the logic of queries against provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Extract and parse the evaluation
            evaluation_text = response.choices[0].message.content.strip()
            
            # Extract JSON from the response
            import re
            json_match = re.search(r'\{[\s\S]*\}', evaluation_text)
            if json_match:
                evaluation_json = json.loads(json_match.group(0))
            else:
                evaluation_json = {
                    "error": "Failed to parse evaluation JSON",
                    "raw_response": evaluation_text
                }
            
            logger.info(f"Generated evaluation: {evaluation_json}")
            return evaluation_json
        
        except Exception as e:
            logger.error(f"Error with OpenAI logic evaluation: {str(e)}")
            raise