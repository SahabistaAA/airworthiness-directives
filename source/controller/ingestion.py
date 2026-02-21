import os
from typing import List

from source.models.document import Document
from source.utils.logger import logger

class IngestionController:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def ingest_documents(self) -> List[Document]:
        documents = []
        if not os.path.exists(self.data_dir):
            logger.error(f"Data directory {self.data_dir} does not exist.")
            return documents

        for filename in os.listdir(self.data_dir):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(self.data_dir, filename)
                logger.info(f"Ingesting file: {filename}")
                
                try:
                    # Ingestion only handles file discovery and metadata creation.
                    # Text extraction is now handled by the ParsingController.
                    doc = Document(
                        file_path=file_path,
                        filename=filename,
                        text="" 
                    )
                    documents.append(doc)
                    logger.info(f"Successfully ingested {filename}")
                except Exception as e:
                    logger.error(f"Failed to ingest {filename}: {e}")

        return documents
