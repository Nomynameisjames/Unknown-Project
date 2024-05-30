#!/usr/bin/env python3
import os
from dotenv import load_dotenv, find_dotenv
from typing import Union, Dict, List
from bson import ObjectId
from pymongo.server_api import ServerApi
from pymongo import MongoClient

load_dotenv(find_dotenv())

"""
    The MongoClient method helps establish a connection to the MongoDB
    cluster, takes the connection string as an argument and returns a connection
    object
"""
connection_str = os.getenv("URL")

class mongo_driver:
    def __init__(self, url: str, db: str, collection: str):
        self.__engine = MongoClient(url, server_api=ServerApi('1'))
        self.__db = self.__engine[db][collection]
        """
            this method returns a connection object that enables the user access
            to a collection in the mongo db dataset, takes two args the db to be
            accessed and the collection(table) within the db
        """
    @property
    def engine(self):
        return self.__engine

    def create(self, dataset: Union[Dict, List]) -> str:
        """
            using the collection object that enables access to the table,
            we utilise the insert_one() method that enables a user save a single data
            with a dict format in the table. Furthermore, the insert_many()
            method takes a list of dict as an argument and save to the db.
            when creating a payload it is ideal to utilise the following format
            { "_id" : <specific id to access the data>
                "any other info" : "data"
                }
            the id key usually prefixed with an underscore help indicate which data
            is to be accessed, if not provided an id is auto generated for the 
            data.
        """
        try:
            if isinstance(dataset, dict):
                user_file = self.__db.insert_one(dataset).inserted_id
            elif isinstance(dataset, list):
                user_file = self.__db.insert_many(dataset).inserted_ids
            else:
                return f"file type must either be a dict or list"
            return f"File saved user_ID is {user_file}"
        except Exception as e:
            return f" some error occured while saving data {e}"

    def search(self, param: str, prefix) -> Union[List, str]:
        """
            Another collection obj method utilised is the find() this take a dict
            as an arg, any key could be used to access the specific data being 
            searched, in this case we take the name of a specific user in the db.
            Furthermore, the find_many() method returns a list of items being searched.
            Notable if an empty dict is passed as an arg in the find({}) method,
            it returns all te data within that collection.
        """
        try:
            if param == "_id":
                prefix = ObjectId(prefix)
            user =  self.__db.find({param: prefix})
            item = [data for data in user if data]
            print("\n\n AWAITING \n")
            if item:
                return item
            return "User not found"
        except Exception as e:
            return f"error {e}"

    def Query_search(self, parameter: str, prefix: str) -> List:
        """
            The find() method can also be used to query the database, when no arg
            is passed it returns the entire dataset in the collection. Furthermore,
            the first arg passed in the method eg find({'name': 'x'}) represent a specific search
            that returns an object which when looped through contains the info that matches the searched item.
            the search can also be tuned to omit or display specific results by passing two args to the method
            where the first arg is the query item and the second arg the data to be omitted or included in the search
            1 is used to represent inclusion while 0 to omit an item eg find ({}, {"name": 1}) this returns the item 
            with only the name preesent in the dataset, to omit the name or anyother key, set the value to 0.
            Finally, certain advanced query symbols are used to search a wider range of item eg 
            find({"name" : {"$gt" : "s"}}) this returns items where the name is greater than s
        """
        user = self.__db.find({parameter: {"$regex": prefix, "$options": "i"}})
        # the query uses the regex modifier to search items within the parameter that matches the prefix
        # the option modifier is used to tune the search wheree the i value indicates casesensitivity and the m indicates enabling a mutiline search
        item = [data for data in user if data]
        return item

    def Update_profile(self):
        pass
