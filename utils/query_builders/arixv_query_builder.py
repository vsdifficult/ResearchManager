from typing import List

class ArxivAIQueryBuilder:
    
    CATEGORIES = {
        "ai": "cs.AI",       
        "ml": "cs.LG",       
        "cv": "cs.CV",       
        "nlp": "cs.CL",      
        "robotics": "cs.RO",
        "multiagent": "cs.MA" 
    }

    def __init__(self):
        self.keywords: List[str] = []
        self.categories: List[str] = []
        self.authors: List[str] = []
        self.exclude_keywords: List[str] = []

    def add_keyword(self, text: str) -> "ArxivAIQueryBuilder":
        clean_text = f'"{text}"' if " " in text else text
        self.keywords.append(clean_text)
        return self

    def add_category(self, cat_alias: str) -> "ArxivAIQueryBuilder":
        if cat_alias in self.CATEGORIES:
            self.categories.append(self.CATEGORIES[cat_alias])
        else:
            raise ValueError(f"Not found category. Usable categories: {list(self.CATEGORIES.keys())}")
        return self

    def add_author(self, author_name: str) -> "ArxivAIQueryBuilder":
        clean_author = f'"{author_name}"' if " " in author_name else author_name
        self.authors.append(f"au:{clean_author}")
        return self

    def exclude_keyword(self, text: str) -> "ArxivAIQueryBuilder":
        clean_text = f'"{text}"' if " " in text else text
        self.exclude_keywords.append(f"NOT {clean_text}")
        return self

    def build(self) -> str:
        parts = []
        
        if self.categories:
            cat_parts = [f"cat:{c}" for c in self.categories]
            parts.append(f"({' OR '.join(cat_parts)})")
            
        if self.keywords:
            parts.append(f"({' AND '.join(self.keywords)})")
            
        if self.authors:
            parts.append(f"({' OR '.join(self.authors)})")
            
        main_query = " AND ".join(parts)
        
        if self.exclude_keywords:
            exclude_query = " AND ".join(self.exclude_keywords)
            if main_query:
                main_query = f"{main_query} AND {exclude_query}"
            else:
                main_query = exclude_query
                
        if not main_query:
            raise ValueError("Query Empty")
            
        return main_query
