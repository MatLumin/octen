import flask;
from flask import Flask
from flask import request
from typing import *
from reserved_addresses import *;

class AuthNode:
    HOLDER_NODES_API_KEYS:List[str] = [
        "HOLDER-12315-45139-74846",
        "HOLDER-24685-87813-81173",
    ];
    def __init__(self):
        pass

    @classmethod
    def is_api_key_valid_for_holder(cls, api_key:str):
        return api_key in cls.HOLDER_NODES_API_KEYS;







if __name__ == "__main__":
    app = Flask("AuthNode");
    auth_node:AuthNode = AuthNode()  

    @app.route("/api/is_api_key_valid_for_holder")
    def api_hh_is_api_key_valid_for_holder():
        api_key = request.json["api_key"];
        return {
            "is_ok":True,
            "data":{
                "is_valid":auth_node.is_api_key_valid_for_holder(api_key=api_key)
            }
        };

            
    app.run(debug=True, host=AUTH_NODE_HOST, port=GLOBAL_PORT)