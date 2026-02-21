import os
from typing import List
from source.models.rule import ADRules
from source.utils.logger import logger

import google.generativeai as genai
from source.config.settings import settings
import yaml
import json

class LLMParser:
    def __init__(self):
        genai.configure(api_key=settings.llm_config.api_key)
        self.model = genai.GenerativeModel(settings.llm_config.model)

    def parse(self, text: str) -> ADRules:
        try:
            with open('source/config/prompts/extraction_prompt.yaml', 'r') as f:
                prompt_template = yaml.safe_load(f)['extraction_prompt']
            
            prompt = prompt_template.replace('{ad_text}', text)
            response = self.model.generate_content(prompt)
            
            res_text = response.text.strip()
            if res_text.startswith("```json"):
                res_text = res_text[7:]
            if res_text.endswith("```"):
                res_text = res_text[:-3]
            res_text = res_text.strip()
            
            data = json.loads(res_text)
            return ADRules(**data)
        except Exception as e:
            logger.error(f"LLM parsing failed: {e}")
            return None