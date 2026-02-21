import os
from typing import List, Dict
from source.controller.ingestion import IngestionController
from source.agent.ads_agent import ADSAgent
from source.controller.evaluation import EvaluationController
from source.models.document import Document
from source.models.aircraft import AircraftConfiguration
from source.utils.logger import logger
from source.utils.json_serializer import JSONSerializer
from source.config.settings import settings

class Pipeline:
    def __init__(self, data_dir: str):
        self.ingestion_controller = IngestionController(data_dir)
        self.ads_agent = ADSAgent()
        self.evaluation_controller = EvaluationController()

    def run(self, aircraft_fleet: List[AircraftConfiguration]) -> Dict[str, Dict[str, bool]]:
        """
        Runs the pipeline: Ingests ADs, Parses them, and Evaluates the fleet against each AD.
        Returns: {ad_id: {msn: is_affected}}
        """
        logger.info("Starting pipeline...")
        
        # 1. Ingestion
        documents = self.ingestion_controller.ingest_documents()
        if not documents:
            logger.warning("No documents found. Pipeline will exit.")
            return {}
        
        results = {}

        for doc in documents:
            logger.info(f"Processing document: {doc.filename}")
            
            # 2. Parsing via Agent
            rules = self.ads_agent.process_document(doc)
            if rules.ad_id == "UNKNOWN" or rules.ad_id == "ERROR":
                logger.warning(f"Could not parse rules for {doc.filename}")
                continue
            
            # 3. Save Structured Output
            output_dir = settings.OUTPUT_DIR if hasattr(settings, 'OUTPUT_DIR') else 'data/output'
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"{rules.ad_id}.json")
            
            with open(output_file, 'w') as f:
                f.write(JSONSerializer.serialize_rules(rules))
            logger.info(f"Saved structured rules to {output_file}")
            
            # 4. Evaluation
            ad_results = {}
            for i, aircraft in enumerate(aircraft_fleet):
                is_affected = self.evaluation_controller.evaluate(rules, aircraft)
                ad_results[i] = is_affected
            
            results[rules.ad_id] = ad_results
        
        logger.info("Pipeline finished.")
        return results
