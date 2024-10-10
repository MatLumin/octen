from __future__ import annotations
from typing import *;

import hashlib;
import time;

import threading;

from flask import Flask;
import flask;
import requests

HexStr = str;

HASH_ALGHO = "sha256"

HOLDER_API_KEYS =  [
    "12345",
    "98765",
]

READ_ONLY_API_KEYS = [
    "abcd",
    "qwer"
]

def is_holder_api_key_valid(key:str)->bool:
    return key in HOLDER_API_KEYS;

def is_read_ony_api_key_valid(api_key:str)->bool:
    return api_key in READ_ONLY_API_KEYS;

class Block:
    def __init__(self):
        self.index = 0;
        self.data:HexStr = "";
        self.unix:int = 0;
        self.prevhash:HexStr = "";

    def hash(self)->HexStr:
        h = hashlib.new(HASH_ALGHO);
        h.update((self.index.__str__()+self.data+self.prevhash+str(self.unix)));
        return h.hexdigest;


  
    def json(self)->Dict[str, Any]:
        return {
            "index":self.index,
            "data":self.data,
            "unix":self.unix,
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




class HolderAddrss:
    def __init__(self):
        self.internet_address = "";
        self.api_key = api_key;

    def get_chain(self, your_api_key:str)->List[Dict[str,Any]]:
        print(f"getting chain from {self.internet_address}");
        r = requests.get(self.internet_address+"/api/get_chain",params=["api_key":your_api_key]);
        print(f"response from {self.hinternet_address}");
        json =  r.json();
        if json["is_ok"] == True:
            return json["data"];
        return [];


class WaitingForValidationTrans:
    def __init__(self, internet_address_of_sender, api_key_of_sender,  uuid, data:HexStr, state:int=False):
        self.internet_address_of_sender = internet_address_of_sender;
        self.api_key_of_sender = api_key_of_sender;
        self.uuid:str = uuid;
        self.data = data;
        self.state = state;
    

    @property
    def not_validated_nor_rejected(self):
        return self.state = 1;
    

    @property
    def validated(self):
        return self.state = 2;
    


    @property
    def rejected(self):
        return self.state = 3;   


    def json(self):
        return {
            "internet_address_of_sender":self.internet_address_of_sender,
            "api_key_of_sender":self.api_key_of_sender,
            "uuid":self.uuid,
            "data":self.data,
        };

class Holder:
    def __init__(self, api_key):
        self.api_key = api_key;
        self.waiting_for_validation:Dict[str,WaitingForValidationTrans] = {};
        self.sent_trans:Dict 
        self.chain = [];
        self.holders = [];


    def get_nth_block(self, n:int)->Block|None:
        if self.chain.__len__() >= n:
            return None;
        else:
            return self.chain[n];


    def get_chain_json()->List[Dict[str,Any]]:
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
                

    def add_waiting_for_validations_trans(self, target:WaitingForValidationTrans)->int:
        """
        return 0 if it new 
        returns 1 if it it exists and not validated nor rejected yet
        return 2 if it exists and is validated
        return 3 if it exists and is rejected
        """
        exists:bool = target.uuid in self.waiting_for_validation:
        if exists == False:
            print("a new transaction!");
            self.waiting_for_validation[target.uuid] = target;
            self.waiting_for_validation[target.uuid].state = 1;
            return 0;

        if exists == True:
            return self.WaitingForValidationTrans["uuid"];

    @property
    def chain_len(self)->int:
        return self.chain.__len__();



    def tell_approvement_of_trans_to_submitter(self, uuid=str)->int:
        """
        -1 means uuid did not exists!
        1 means ok
        """
        if uuid not in self.waiting_for_validation:
            print(f"transaction of {uuid} does not exist in here!");
            return -1;
        trans:WaitingForValidationTrans = self.waiting_for_validation[uuid];
        internet_address_off_sender:str = trans.internet_address_of_sender;
        requests.get(internet_address_off_sender+"/api/know_trans_as_approved/", params={"uuid":uuid});
        return 1;


    def on_trans_being_approved(self, uuid:str)->int:



def update_holder(holder:Holder):
    print("started the tred of chain updator")
    while True:
        time.sleep(5);
        holder.update_chain();

holder:Holder = Holder(api_key=input("ENTER_API_KEY:"));
app = Flask("holder");



chain_updater_thread = threading.Thread(target=update_holder, args=holder, daemon=True)
chain_updater_thread.start();




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
    target = WaitingForValidationTrans(internet_address_of_sender=internet_address_of_sender, api_key_of_sender=api_key_of_sender, uuid=uuid, data=data, state=1);
    return {"is_ok":True, "msg":"all is ok", "data":holder.add_waiting_for_validations_trans()}; 


@app.get("/api/approve_trans")
def hh4():
    uuid = flask.request.args.get("uuid");
    if uuid == None:
        return {"is_ok":False, "msg":"uuid is missing",};
    holder.tell_approvement_of_trans_to_submitter(uuid=uuid);




@app.get("/api/reject_trans")
def hh4():
    pass



