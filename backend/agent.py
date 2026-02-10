import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGAgent:
    """
    Mock Retrieval-Augmented Generation (RAG) Agent
    This class simulates retrieval + generation logic
    (No real LLM or vector database is used)
    """

    def __init__(self):
        logger.info("RAGAgent initialized")

    def retrieve_context(self, query: str) -> str:
        """
        Simulates retrieving relevant context for a query
        """
        logger.info(f"Retrieving context for query: {query}")
        return f"Mock context related to '{query}'"

    def generate_answer(self, query: str, context: str) -> str:
        """
        Simulates answer generation using query + context
        """
        logger.info("Generating answer")
        return (
            f"Answer generated for query '{query}' "
            f"using context '{context}'"
        )

    def run(self, query: str) -> str:
        """
        Complete RAG flow: retrieve context → generate answer
        """
        logger.info("Running RAG pipeline")
        context = self.retrieve_context(query)
        response = self.generate_answer(query, context)
        return response
