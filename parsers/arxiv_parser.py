import logging
import xml.etree.ElementTree as ET
from typing import Dict, List, Union
import httpx
from ..utils.query_builders.arixv_query_builder import ArxivAIQueryBuilder

class AsyncArxivParser: 
    def __init__(self, 
                 client: httpx.AsyncClient, 
                 logger: logging.Logger,
                 query: Union[str, ArxivAIQueryBuilder], 
                 max_results: int = 10):
        self.client = client 
        self.logger = logger
        self.max_results = max_results
        self.base_url = "https://arxiv.org"
        
        if isinstance(query, ArxivAIQueryBuilder):
            self.query = query.build()
        else:
            self.query = query

    async def __call__(self) -> List[Dict[str, str]]:
        params = {
            "search_query": self.query,
            "max_results": self.max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        
        try:
            response = await self.client.get(self.base_url, params=params)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            self.logger.error(f"HTTP error occurred while querying arXiv: {exc}")
            raise RuntimeError(f"Arxiv API connection failed: {exc}")

        root = ET.fromstring(response.text)
        ns = {'atom': 'http://w3.org'}
        entries = root.findall('atom:entry', ns)
        
        if not entries: 
            self.logger.warning(f"Arxiv API did not find any papers for query: {self.query}")
            raise RuntimeError(f"Arxiv API did not find any papers for query: {self.query}")
            
        self.logger.info(f"Successfully found {len(entries)} papers for query: {self.query}")
        
        parsed_papers = []
        for entry in entries:
            title_node = entry.find('atom:title', ns)
            id_node = entry.find('atom:id', ns)
            
            title = " ".join(title_node.text.split()) if title_node is not None and title_node.text else "No Title"
            abstract_url = id_node.text.strip() if id_node is not None and id_node.text else ""
            
            pdf_url = ""
            for link in entry.findall('atom:link', ns):
                if link.attrib.get('title') == 'pdf' or link.attrib.get('type') == 'application/pdf':
                    pdf_url = link.attrib.get('href', '')
                    break
            
            parsed_papers.append({
                "title": title,
                "abstract_url": abstract_url,
                "pdf_url": pdf_url
            })
            
        return parsed_papers
