from NodeRoutingData import NodeRoutingData;

class AuthNodeRoutingData(NodeRoutingData):
    def __init__(self, host, port, uti):
        NodeRoutingData.__init__(self, host=host, port=port, uti=uti)