import requests;
from requests import Response

class NodeRoutingData:
    def __init__(self, host:str, port:str, uti:str):
        self.host = host;
        self.port = port;
        self.uti = uti;
    
    def url_origin(self)->str:
        return f"http://{self.host}:{self.port}/"

    def is_online(self)->bool:
        try:
            response:Response = requests.get(timeout=1, url=self.url_origin()+"ui/about")
        except:
            return False
        return response.status_code == 200;
    