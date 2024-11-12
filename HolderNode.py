import sys;

from flask import Flask, render_template, request;

from HolderRoutingData import HolderRoutingData;

from reserved_addresses import *;

from access_keys import *;


class HolderNode:
    def __init__(self, host:str, port:int, uti:str, api_key:str):
        self.self_routing_data = HolderRoutingData(host=host, port=port, uti=uti)
        self.api_key = api_key;







if __name__ == "__main__":
    host = sys.argv[1];
    port = GLOBAL_PORT;
    uti = sys.argv[2];
    api_key = sys.argv[3];
    app = Flask("HolderNode");
    holder_node:HolderNode = HolderNode(host=host, uti=uti, port=GLOBAL_PORT, api_key=api_key)

    @app.route("/ui/about")
    def ui_hh_about():
        return render_template("HolderNode__about", holder_node=holder_node)
    

    @app.route("/api/get_key")
    def ui_hh_get_key():
        router_access_key = request.json["router_access_key"] == ROUTER_ACCESS_KEY
        return {
            "is_ok":True,
            "data":{
                "api_key":holder_node.api_key
            }
            }



    app.run(host=host, port=port, debug=True)