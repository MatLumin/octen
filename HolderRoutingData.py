from typing import *;
from requests import get, Response
from NodeRoutingData import NodeRoutingData;

from reserved_addresses import *;


class HolderRoutingData(NodeRoutingData):
    def __init__(self, uti:str, host:str, port:int):
        NodeRoutingData.__init__(self, uti=uti, port=port, host=host)

    def is__valid_by_auth_for_holder(self, router_access_key:str):
        
        if self.is_online() == False:
            print(f"skipping key validation for holder {self.host} {self.uti} since its not available");
            return False;
        #1.ASK THE HOLDER FOR ITS API KEY
        #2.ASK THE AUTH FOR VALIDATION
        #!ONLY ROUTER CAN ACCESS THIS METHOD!
        api_key:str = "";

        response:Response = get("http://"+self.host+":"+str(self.port)+"/api/get_key", json={"router_access_key":router_access_key});
        
        print(response.text)
        
        api_key = response.json()["data"]["api_key"]

        response = get("http://"+AUTH_NODE_HOST+":"+str(GLOBAL_PORT)+"/api/is_api_key_valid_for_holder", json={"api_key":api_key});
        output =  response.json()["data"]["is_valid"]
        print("================")
        return output;








    
