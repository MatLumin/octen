from typing import *;

from HolderRoutingData import HolderRoutingData;
from AuthNodeRoutingData import AuthNodeRoutingData;

from AuthNode import AuthNode;
from HolderNode import HolderNode;

from flask import Flask;
from flask import render_template, redirect;

from collections import OrderedDict;

from reserved_addresses import *
from access_keys import *;


class RouterNode:
    def __init__(self):
        self.holders:List[HolderRoutingData] = [
            HolderRoutingData(host="127.0.1.4", port=GLOBAL_PORT, uti="holder_1"),
            HolderRoutingData(host="127.0.1.5", port=GLOBAL_PORT, uti="holder_2"),
            HolderRoutingData(host="127.0.1.6", port=GLOBAL_PORT, uti="holder_3"),
        ]
        self.auth:AuthNodeRoutingData = AuthNodeRoutingData(host=AUTH_NODE_HOST, port=GLOBAL_PORT, uti="auth_1");





if __name__ == "__main__":
    app = Flask("RouterNode")
    router_node:RouterNode = RouterNode()

    @app.route("/")
    def hh_index():
        return "meow"
        
    #user interface 
    @app.route("/ui/network_routes")
    def ui_hh_holder_report():
        return render_template("RouterNode__network_routes.html", holders=router_node.holders, authnode=router_node.auth, ROUTER_ACCESS_KEY=ROUTER_ACCESS_KEY);
        


    #api 
    @app.route("/api/network_routes")
    def api_hh_holder_list():
        j:List[Dict[str,Any]] = []
        i1:HolderRoutingData
        for i1 in router_node.holders:j.append(i1.json())
        return {
                "is_ok":True,
                "data":{
                    "holders":j,
                },
                
                }
  
    app.run(debug=True, host=ROUTER_NODE_HOST, port=GLOBAL_PORT);