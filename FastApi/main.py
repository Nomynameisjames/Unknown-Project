#!/usr/bin/env python3
import json
from functools import lru_cache
from fastapi import FastAPI
from MongoDB.LearnMongoDB import connection_str, mongo_driver
from pydantic import BaseModel

app = FastAPI()

engine = mongo_driver(connection_str, "User", "Users_profile")
template = None
with open("../MongoDB/user_profile.json", 'r') as data:
    template = json.load(data)

class User(BaseModel):
    name: str
    username: str
    email: str
    password: str


@app.post("/users/signup")
async def signup(user: User):
    names = None
    if template is None:
        return {"message": "template not found"}
    existing_names = engine.search("name", user.name)
    if isinstance(existing_names, list):
        names = [name for name in existing_names if name.get("name") == user.name]
    if names:
        return {"message": "user already exists"}
    template["name"] = user.name
    template["username"] = user.username
    template["password"] = user.password
    template["email"] = user.email
    save = engine.create(template)
    return save


"""
    using a route that takes in an argument
"""
@lru_cache(maxsize=None)
@app.get("/users/{ID}")
async def root(ID: str):
    data = engine.search("_id", ID)
    user_file = None
    for item in data:
        if isinstance(item, str):
            item = {"message": data}
        else:
            item.pop("_id")
        user_file = item
    return user_file if user_file else {"status" : "Failed"}


"""
    FastAPI file path parameter
"""
@app.get("/books/{file_path:path}")
async def books(file_path: str):
    return {"file_path": file_path}


