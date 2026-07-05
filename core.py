import requests, arxiv, logging

class ResearchManager: 

    def __init__(self, 
                 session: requests.Session,
                 logger: logging.Logger): 
        self.session = session 
        self.logger = logger

    def init_manager(self): 
        self.logger.log(msg="Init Manager Started") 
        response = requests.get("https://google.com") 
        if response.status_code == 200: 
            self.logger.log(level=logging.INFO, msg="Google 200") 

        else: 
            self.logger.log(level=logging.WARNING, msg="Failed connect") 
            raise requests.exceptions.ConnectionError() 
        
    def parse(self): 
        pass 


        
        