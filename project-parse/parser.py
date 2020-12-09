from bs4 import BeautifulSoup
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import datetime

from pars import parse

def pars(id: str):
    return parse(db_reg_req[id]["region"], db_reg_req[id]["request"])


def insert_in_history(id: str):
    help = {str(datetime.datetime.now().timestamp()): pars(id)}
    if id in db_history_by_id:
        db_history_by_id[id].update(help)
    else:
        db_history_by_id.update({id: help})


db_reg_req = {
    "0": {"id": "0", "region": "rossiya", "request": "книга"},
    "1": {"id": "1", "region": "mordoviya", "request": "fifa"},
}
db_history_by_id = {
    "0": {"1607498786": 1147168, "1607499005": 1147143}
}

def gen_key():
    key = 0
    while db_reg_req.get(str(key)) != None:
        key += 1
    print(key)
    return str(key)

app = FastAPI()


class Item_inp(BaseModel):
    region: str
    request: str


class Item_hist(BaseModel):
    id: str = None
    time1: str
    time2: str


@app.get("/")
async def root():
    return {"message": pars("0")}


@app.get("/stat/")
async def parse_hist(item: Item_hist):
    ts1 = datetime.datetime.strptime(item.time1, "%Y-%m-%d %H:%M:%S").timestamp()
    ts2 = datetime.datetime.strptime(item.time2, "%Y-%m-%d %H:%M:%S").timestamp()
    result = {}    
    for time, count in db_history_by_id[item.id].items():
        if float(time) > ts1 and float(time) < ts2:
            result[int(time)] = count
    return result


@app.get("/add/{item_id}")
async def read_item(item_id: str):
    if item_id not in db_reg_req:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_reg_req[item_id]


@app.get("/add/")
async def see_all():
    return db_reg_req


@app.post("/add/")
async def create_item(item: Item_inp):
    item_id = gen_key()
    db_reg_req[item_id] = {"id": item_id, "region": item.region, "request": item.request}
    return item_id
