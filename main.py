"""
ALL REQUESTS DO REQUIRE THE API KEY!
"""

from __future__ import annotations
from typing import *;
import hashlib;
import time;
import random;
import threading;

from flask import Flask;
import flask;
import requests
import jinja2
from jinja2 import Template


HexStr = str;

HASH_ALGHO = "sha512"

HOLDER_API_KEYS =  [
    "12345",
    "98765",
]

READ_ONLY_API_KEYS = [
    "abcd",
    "qwer"
]

def generate_uuid()->str:
    output = "";
    c= random.choice;
    for i1 in range(4):
        output += c("qwrtpsdfghjklzxcvbnm") + c("auioe") + c("qwrtpsdfghjklzxcvbnm") + "-"
    return output

def is_holder_api_key_valid(key:str)->bool:
    return key in HOLDER_API_KEYS;

def is_read_ony_api_key_valid(api_key:str)->bool:
    return api_key in READ_ONLY_API_KEYS;


def pow_approver(produced_hash:HexStr)->bool:
    count = 0;
    for i1 in produced_hash:
        zero_count += i1 == "a" ;
    return count > 14;

def return_file_content(path:str)->str:
    with open(path, mode="r", encoding="utf-8") as f1:
        return f1.read();

def file_as_template(path:str)->jinja2.Template:
    return jinja2.Template(return_file_content(path=path));



class Block:
    def __init__(self):
        self.index = 0;
        self.data:HexStr = "";
        self.unix:int = 0;
        self.nonce:int = 0;
        self.prevhash:HexStr = "";

    def hash(self)->HexStr:
        h = hashlib.new(HASH_ALGHO);
        h.update(self.bcontent);
        return h.hexdigest;

    def find_nonce(self)->int:
        nonce = 0;
        while True:
            self.nonce = nonce;
            if pow_approver(hash()) == True:
                return nonce;

  
    def json(self)->Dict[str, Any]:
        return {
            "index":self.index,
            "data":self.data,
            "unix":self.unix,
            "nonce":self.nonce,
            "prevhash":self.prevhash,
        };


    @classmethod
    def convert_block_json_array_into_blocks(cls, input_data:List[Dict[str,Any]])->List[Block]:
        output:List[Block] = [];
        for i1 in input_data:
            sub_data = cls();
            sub_data.index = i1["index"];
            sub_data.data = i1["data"];
            sub_data.unix = i1["unix"];
            sub_data.prevhash = i1["prevhash"];
        return output;


    @property
    def bcontent(self)->bytes:
        return (self.index.__str__()+self.data+self.prevhash+str(self.unix)+str(self.nonce)).encode("utf-8")




class HolderAddrss:
    def __init__(self, internet_address, api_key):
        self.internet_address = internet_address;
        self.api_key = api_key;

    def get_chain(self, your_api_key:str)->List[Dict[str,Any]]:
        print(f"getting chain from {self.internet_address}");

        r = requests.get(
            self.internet_address+"/api/get_chain",
            params={"api_key":your_api_key}
            );
        
        print(f"response from {self.hinternet_address}");
        json =  r.json();
        if json["is_ok"] == True:
            return json["data"];
        return [];

    def send_block(self, block:Block, your_api_key:str):
        print(f"sending the block into {self.internet_address} of api_key of {self.api_key}");
        json_to_send = {"block":block.json()};
        json_to_send["api_key"] = your_api_key;
        res = requests.post(self.internet_address+"/api/add_block", json=json_to_send);
        print(f"sending the block into {self.internet_address} of api_key of {self.api_key} was this {res.json()}");


    def ask_for_trans_approval(self, trans:InternalTransRequest, your_api_key):
        print(f"asking for approval of {uuid} from {self.api_key} {self.internet_address}");
        json_to_send:Dict = {"trans":InternalTransRequest.json_lite(), "api_key":your_api_key};
        requests.post(self.internet_address+"/ask_for_trans_approval", json=json_to_send);


        
        


class ExternalTransRequest:
    def __init__(self, internet_address_of_sender, api_key_of_sender,  uuid, data:HexStr, state:int=False):
        self.internet_address_of_sender = internet_address_of_sender;
        self.api_key_of_sender = api_key_of_sender;
        self.uuid:str = uuid;
        self.data = data;
        self.state = state;
    

    @property
    def not_validated_nor_rejected(self):
        return self.state == 1;
    

    @property
    def validated(self):
        return self.state == 2;
    


    @property
    def rejected(self):
        return self.state == 3;   


    def json(self):
        return {
            "internet_address_of_sender":self.internet_address_of_sender,
            "api_key_of_sender":self.api_key_of_sender,
            "uuid":self.uuid,
            "data":self.data,
        };



class InternalTransRequest:
    def __init__(self, data:HexStr, uuid:str):
        self.data = data;
        self.uuid = uuid;
        self.approvers = [] #api keys those who approved


    def add_approver(self, api_key)->0:
        """
        0 -> already exists
        1 -> ok
        """
        if api_key in self.approvers:
            return 0;
        self.approvers.append(api_key);
        return 1;


    def json(self)->Dict[str, Any]:
        return {
            "data":self.data,
            "uuid":self.uuid,
            "approvers":self.approvers,
            };

    def json_lite(self):
         #like json but without approvers.
         return {
            "data":self.data,
            "uuid":self.uuid,
            };       

    @property 
    def approvers_count(self)->int:
        return self.approvers.__len__();





class Holder:
    def __init__(self, api_key):
        self.api_key = api_key;
        self.external_trans_request:Dict[str,ExternalTransRequest] = {};
        self.internal_trans:Dict[str, InternalTransRequest] = {};
        self.chain = [];
        self.holders = [];


    def get_nth_block(self, n:int)->Block|None:
        if self.chain.__len__() >= n:
            return None;
        else:
            return self.chain[n];


    def get_chain_json(self)->List[Dict[str,Any]]:
        output = [];
        block:Block;
        for block in self.chain:
            output.append(
                block.json()
            );
        return output;





    def update_chain(self)->None:
        print("lets update the chain....")
        holder:HolderAddrss;
        for holder in self.holders:
            chain = holder.get_chain(your_api_key=self.api_key);
            print(f"self chain len = {self.chain_len} ; {holder.internet_address}'s len = {chain.__len__()}");
            if chain.__len__() > self.chain_len:
                print(f"setting chain of {holder.internet_address} as self chian now");
                self.chain = Block.convert_block_json_array_into_blocks(chain);
        return None;
                

    def add_external_trans_request(self, target:ExternalTransRequest)->int:
        """
        return 0 if it new 
        returns 1 if it it exists and not validated nor rejected yet
        return 2 if it exists and is validated
        return 3 if it exists and is rejected
        """
        exists:bool = target.uuid in self.external_trans_request;
        if exists == False:
            print("a new transaction!");
            self.external_trans_request[target.uuid] = target;
            self.external_trans_request[target.uuid].state = 1;
            return 0;

        if exists == True:
            return self.external_trans_request["uuid"];





    def tell_approvement_of_trans_to_submitter(self, uuid=str)->int:
        """
        -1 means uuid did not exists!
        1 means ok
        """
        if uuid not in self.external_trans_request:
            print(f"transaction of {uuid} does not exist in here!");
            return -1;
        trans:ExternalTransRequest = self.external_trans_request[uuid];
        internet_address_off_sender:str = trans.internet_address_of_sender;
        requests.get(internet_address_off_sender+"/api/know_trans_as_approved/", params={"uuid":uuid});
        return 1;



    def on_trans_being_approved(self, uuid:str, who_api_key:str)->int:
        """
        -1 -> uuid did not exist!
        0 -> api key already approved me
        1 -> ok
        2 -> ok and tranaction is approved by more than 51%
        """
        if uuid not in self.internal_trans:
            print(f"internal trans of {uuid} did not exist for approval");
            return -1;

        target:InternalTransRequest =  self.internal_trans[uuid];
        if uuid in target.approvers:
            print(f"api key of {who_api_key} has already approved {uuid}!");
            return 0;

        target.add_approver(api_key=who_api_key);

        if self.calculate_approval_ratio_for_internal_trans(uuid=uuid) >= 0.51:
            
            self.blockify_and_broadcast_trans(uuid=uuid);

        return 1;


    def on_trans_being_rejected(self, uuid:str, who_api_key:str)->int:
        print(f"{who_api_key} disapproved the {uuid}; we dont care btw");
    

    def calculate_approval_ratio_for_internal_trans(self, uuid:str)->float:
        """
        -1.0 trans not found
        """
        if uuid not in self.internal_trans:
            print(f"internal trans of {uuid} does not exist! we cant calcualte network approval for it");
            return -1;
        return self.internal_trans[uuid].approvers_count / self.holder_count;


    def blockify_and_broadcast_trans(self, uuid:str)->None|Block:
        if uuid not in self.internal_trans:
            print("internal trans of {uuid} does not exsit; we cant blockfiy it!")
            return None;
        block:Block = self.blockify_internal_trans(uuid=uuid);
        self.add_block(block=block);
        self.broadcast_block(block=block);
    
    

    def blockify_internal_trans(self, uuid:str)->Block:
        internal_trans:InternalTransRequest = self.internal_trans[uuid];
        output:Block = Block();
        output.index = self.new_chain_block_index;
        output.data = internal_trans.data;
        output.unix = time.time_ns();
        output.nonce = 0;
        output.prevhash = self.prev_hash();
        output.find_nonce();
        del self.internal_trans[uuid];
        return output;


    def broadcast_block(self, block:Block):
        holder:Holder;
        for holder in self.holders:
            holder.send_block(block, your_api_key=self.api_key);

            
    def add_block(self, block:Block):
        #adds the block with no question like a good boy
        self.chain.append(block);
    
    def add_internal_trans(self, data:HexStr)->str:
        #returns uuid
        generate_uuid:str = generate_uuid();
        InternalTransRequest(data=data, uuid=generate_uuid);
        return generate_uuid;

    def broadcast_internal_trans(self, uuid:str):
        holder:HolderAddrss;
        for hodler in self.holders:
            holder.ask_for_trans_approval(uuid=uuid, your_api_key=self.api_key);

    

    @property
    def chain_len(self)->int:
        return self.chain.__len__();

    @property
    def new_chain_block_index(self)->int:
        return self.chain_len;

    @property 
    def holder_count(self)->int:
        return self.holders.__len__();

    @property 
    def prev_hash(self)->HexStr:
        return self.last_block.hash();
    
    @property 
    def last_block(self)->Block:
        return self.chain[-1];
    


"""def update_holder(holder:Holder):
    print("started the tred of chain updator")
    while True:
        time.sleep(5);
        holder.update_chain();"""

print(HOLDER_API_KEYS)
holder:Holder = Holder(api_key=input("ENTER_API_KEY:"));
app = Flask("holder");



"""chain_updater_thread = threading.Thread(target=update_holder, args=(holder,), daemon=True)
chain_updater_thread.start();"""



@app.get("/api/add_trans")
def hh0():
    api_key:str = flask.request.args.get("api_key");
    if api_key == None:
        return {"is_ok":False, "msg":"api_key_is_missing"};
    if is_holder_api_key_valid(api_key) == False:
        return {"is_ok":False, "msg":"api_key_is_invalid"};
    data:HexStr = flask.requ
    uuid:str = holder.add_internal_trans(data);
    holder.broadcast_internal_trans(uuid=uuid);



@app.get("/api/get_n_block")
def hh_1():
    api_key:str = flask.request.args.get("api_key");
    b:bool = is_read_ony_api_key_valid(api_key);
    if b == False:
        return {"is_ok":False, "msg":"api key is invalid"}
    if b == True:
        target:Block = holder.get_nth_block_json();
        if target == None:
             return {"is_ok":False, f"msg":"block {n} did not exists"}
        else:
            return {"is_ok":True, f"msg":"things aare ok", "data":target.json()};



@app.get("/api/get_chain")
def hh_2():
    if is_holder_api_key_valid(flask.request.args.get("api_key")) == False:
        return {"is_ok":False, "msg":"api key is invalid"};
    return {"is_ok":True, f"msg":"things are ok", "data":holder.get_chain_json()};


@app.get("/api/add_trans")
def hh3():
    if is_holder_api_key_valid(flask.request.args.get("api_key")) == False:
        return {"is_ok":False, "msg":"api key is invalid"};
    internet_address_of_sender = flask.request.remote_addr;
    api_key_of_sender = flask.request.args.get("api_key");
    uuid = flask.request.args.get("uuid");
    if uuid == None:
        return {"is_ok":False, "msg":"uuid is missing!"};
    data = flask.request.args.get("data")
    if data == None:
        return {"is_ok":False, "msg":"data is missing!"}; 
    target = ExternalTransRequest(internet_address_of_sender=internet_address_of_sender, api_key_of_sender=api_key_of_sender, uuid=uuid, data=data, state=1);
    return {"is_ok":True, "msg":"all is ok", "data":holder.add_external_trans_request()}; 


@app.get("/api/approve_trans")
def hh4():
    uuid = flask.request.args.get("uuid");
    if uuid == None:
        return {"is_ok":False, "msg":"uuid is missing",};
    holder.tell_approvement_of_trans_to_submitter(uuid=uuid);


@app.post("/api/add_block")
def hh5():
    api_key = flask.request.args.get("api_key");
    if api_key == None:
        return {"is_ok":False, "msg":"api key is missing"};
    block_raw:Dict[str,Any] = flask.request.args.get("block");
    if block_raw == None:
        return {"is_ok":False, "msg":"block_data_is_missing"};
    block_fields = [
        "index",    
        "data", 
        "unix", 
        "nonce",    
        "prevhash", 
        ];
    for field_name in block_fields:
        field_value = block_raw.get(field_name);
        if field_value == None:
            return {
                "is_ok":False,
                "msg":f"field_{field_name}_is_missing"
            }
    block:Block = Block();
    block.index = block_raw["index"];
    block.data = block_raw["data"];
    block.unix = block_raw["unix"];
    block.nonce = block_raw["nonce"];
    block.prevhash = block_raw["prevhash"];
    holder.add_block(block);


@app.get("/ui/index")
def hh6():
    template:Template = file_as_template("./webpages/holder/index.html");
    return template.render({"holder":holder});






