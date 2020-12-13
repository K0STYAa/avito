from bs4 import BeautifulSoup
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import datetime
import json
from fastapi.middleware.cors import CORSMiddleware

from app.api.pars import parse, parse_top


def pars(id: str):

    return parse(db_reg_req[id]["region"], db_reg_req[id]["request"])


def pars_top(id: str):

    return parse_top(db_reg_req[id]["region"], db_reg_req[id]["request"])


def pars_and_insert_in_history(id: str):

    help = {str(datetime.datetime.now().timestamp()): pars(id)}
    if id in db_history_by_id:
        db_history_by_id[id].update(help)
    else:
        db_history_by_id.update({id: help})

    help = {str(datetime.datetime.now().timestamp()): pars_top(id)}
    if id in top5_posts:
        top5_posts[id].update(help)
    else:
        top5_posts.update({id: help})


def update_all():

    for key in db_reg_req.keys():
        pars_and_insert_in_history(key)

    print(db_history_by_id)

    with open('app/api/db_history_by_id.json', 'w') as outfile:
        json.dump(db_history_by_id, outfile, ensure_ascii=False, indent=4)
    outfile.close()

    with open('app/api/top5_posts.json', 'w') as outfile:
        json.dump(top5_posts, outfile, ensure_ascii=False, indent=4)
    outfile.close()


with open('app/api/db_reg_req.json') as f:
    db_reg_req = json.load(f)
f.close()

with open('app/api/db_history_by_id.json') as f:
    db_history_by_id = json.load(f)
f.close()

with open('app/api/top5_posts.json') as f:
    top5_posts = json.load(f)
f.close()


def gen_key():

    with open('app/api/db_reg_req.json') as f:
        db_reg_req = json.load(f)
    f.close()

    key = 0
    while db_reg_req.get(str(key)) is not None:
        key += 1

    return str(key)


def get_app():

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = get_app()


class Item_inp(BaseModel):
    region: str
    request: str


class Item_hist(BaseModel):
    id: str = None
    time1: str
    time2: str


@app.get("/")
async def root():

    return {"message": "Welcome to my app!"}


@app.get("/stat/")
async def parse_hist(item: Item_hist):

    with open('app/api/db_history_by_id.json') as f:
        db_history_by_id = json.load(f)
    f.close()

    ts1 = datetime.datetime.strptime(
        item.time1, "%Y-%m-%d %H:%M:%S").timestamp()
    ts2 = datetime.datetime.strptime(
        item.time2, "%Y-%m-%d %H:%M:%S").timestamp()

    result = {}

    for time, count in db_history_by_id[item.id].items():
        if float(time) > ts1 and float(time) < ts2:
            result[float(time)] = count

    return result


@app.get("/add/{item_id}")
async def read_item(item_id: str):

    with open('app/api/db_reg_req.json') as f:
        db_reg_req = json.load(f)
    f.close()

    if item_id not in db_reg_req:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_reg_req[item_id]


@app.get("/add/")
async def see_all():

    with open('app/api/db_reg_req.json') as f:
        db_reg_req = json.load(f)
    f.close()

    return db_reg_req


@app.post("/add/")
async def create_item(item: Item_inp):

    with open('app/api/db_reg_req.json') as f:
        db_reg_req = json.load(f)
    f.close()

    for value in db_reg_req.values():
        if value["region"] == item.region and value["request"] == item.request:
            return value["id"]

    item_id = gen_key()

    db_reg_req[item_id] = {
        "id": item_id,
        "region": item.region,
        "request": item.request}

    with open('app/api/db_reg_req.json', 'w') as outfile:
        json.dump(db_reg_req, outfile, ensure_ascii=False, indent=4)
    outfile.close()

    return item_id


@app.get("/top5/{item_id}")
async def read_top5(item_id: str):

    with open('app/api/top5_posts.json') as f:
        top5_posts = json.load(f)
    f.close()

    if item_id not in top5_posts:
        raise HTTPException(status_code=404, detail="Item not found")

    time = list(top5_posts[item_id].keys())[-1]
    return {time: top5_posts[item_id][time]}
