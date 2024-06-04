#!/usr/bin/env python3
from fastapi import FastAPI
from MongoDB.LearnMongoDB import connection_str, mongo_driver
app = FastAPI()

engine = mongo_driver(connection_str, "User", "Users_profile")
#ID = "6656c79494be835141560d09"
#data = engine.search("_id", ID)



"""
    using a route that takes in an argument
"""
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


