import logging
from typing import Dict, List, Any
import httpx
from .shared.enums.resources_enum import TypeOfResource 
from .parsers.arxiv_parser import AsyncArxivParser

class ResearchManager: 
    def __init__(self, 
                 client: httpx.AsyncClient,
                 logger: logging.Logger,
                 query: str,
                 max_results: int = 10): 
        self.client = client 
        self.logger = logger
        self.query = query
        self.max_results = max_results

    async def init_manager(self) -> None: 
        self.logger.info("Init Manager Started") 
        try:
            response = await self.client.get("https://google.com") 
            if response.status_code == 200: 
                self.logger.info("Connectivity healthcheck passed: Google 200") 
            else:
                self.logger.warning(f"Unexpected healthcheck status: {response.status_code}")
                raise httpx.ConnectError("Failed connectivity validation check")
        except httpx.HTTPError as exc:
            self.logger.error(f"Failed to connect to fallback health check link: {exc}")
            raise

    async def parse(self, resource: TypeOfResource) -> List[Dict[str, Any]]: 
        if resource == TypeOfResource.ARXIV: 
            arxiv_parser = AsyncArxivParser(
                client=self.client, 
                logger=self.logger, 
                query=self.query, 
                max_results=self.max_results
            ) 
            
            papers_data = await arxiv_parser()
            
            return [{
                "resource_type": "arxiv",
                "data": papers_data
            }]
            
        else: 
            self.logger.warning(f"Resource type not supported: {resource}")
            raise ValueError(f"Resource type '{resource}' is not recognized in default engine configuration")
