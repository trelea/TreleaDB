from typing import Self
import time
import platform
import os
import json
import uuid

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend



class TreleadbClient:
    def __init__(self, dbName: str, dbPath: str = None, secretKey: str = None) -> None:
        self.__dbName = dbName
        self.__collection: str = None
        self.__secretKey: str = None
        self.data: list = []

        self.__updateQuery: bool = False
        self.__getQuery: bool = False

        if (secretKey):
            self.__secretKey = hashes.Hash(hashes.SHA256(), backend=default_backend())
            self.__secretKey.update(bytes(secretKey.encode()))
            self.__secretKey = base64.urlsafe_b64encode(self.__secretKey.finalize())

        if (dbPath and os.path.exists(dbPath)):
            self.__dbPath = os.path.join(dbPath, 'treleadb')
        if (not dbPath and platform.system() == "Linux"):
            self.__dbPath = os.path.join(os.path.expanduser('~'), 'treleadb')
        if (not dbPath and platform.system() == "Windows" ):
            self.__dbPath = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'treleadb')
        if (not os.path.exists(os.path.join(self.__dbPath, self.__dbName))):
            raise Exception (f"Invalid Specifications For Database '{dbName}'")
        


    def __ReadCollection__(self, collName: str) -> dict:
        with open(os.path.join(self.__dbPath, self.__dbName, f'{collName}.json'), 'r') as _f:
            if (self.__secretKey == None):
                data = json.loads(_f.read())
            else:
                data = Fernet(self.__secretKey).decrypt(_f.read().encode('utf-8'))
                data = json.loads(data.decode('utf-8'))
            _f.close()
        
        return data



    @staticmethod
    def __Validate__Where__Query__Lists__(list1: list, list2: list, __res: bool = True) -> bool:
        for _i in list1:
            if _i not in list2:
                __res = False
        return __res



    def getCollections(self) -> list:
        return list(_.replace('.json', '') for _ in os.listdir(os.path.join(self.__dbPath, self.__dbName)))



    def getCollection(self, collName: str, Schema: bool = False) -> dict:
        if (f'{collName}.json' not in os.listdir(os.path.join(self.__dbPath, self.__dbName))):
            raise Exception (f"Collection '{collName}' Not Found In Database '{self.__dbName}'")

        data = self.__ReadCollection__(collName)

        if (not Schema):
            data = data['Data']
        return data



    def select(self, collName: str) -> Self:
        if (not os.path.exists(os.path.join(self.__dbPath, self.__dbName, f'{collName}.json'))):
            raise Exception (f"Collection '{collName}' Not Found In '{self.__dbName}' Database.")
        self.__collection = collName
        self.data.clear()
        return self
    


    def get(self, **keys: bool) -> Self:
        if (not self.__collection):
            raise Exception (f"No Collesction Has Been Selected")
        
        collection = self.__ReadCollection__(self.__collection)

        if (not all(_ in list(collection['Schema'].keys()) for _ in list(keys.keys()))):
            raise Exception (f"Invalid Keys '{keys}' For Collection '{self.__collection}' In Database '{self.__dbName}'")
        
        self.__getQuery = True
        self.__updateQuery = False

        if (not len(keys)):
            self.data = collection['Data']
            return self
        
        validKeys = [_ for _ in keys if keys[_]]
        for _ in collection['Data']:
            dataRow = dict((key, val) for key, val in _.items() if key in validKeys)
            self.data.append(dataRow)

        return self



    def where(self, *keys: dict) -> Self:
        if (not self.__collection):
            raise Exception (f"No Collesction Has Been Selected")
        
        collection = self.__ReadCollection__(self.__collection)

        if (not self.data):
            raise Exception (f"Invalid Operation In Collection '{self.__collection}' From Database '{self.__dbName}'")
        for _ in keys:
            if (not all(_ in list(collection['Schema'].keys()) for _ in list(_.keys()))):
                raise Exception (f"Invalid Keys '{keys}' For Collection '{self.__collection}' In Database '{self.__dbName}'")
        
        if (self.__getQuery):
            dataKeys = list(self.data[0].keys())
            self.data.clear()
            for _ in keys:
                for object in collection['Data']:
                    if (TreleadbClient.__Validate__Where__Query__Lists__(list(_.values()), list(object.values()))):
                        _temp = {}
                        for d in dataKeys:
                            _temp[d] = object[d]
                        self.data.append(_temp)

        if (self.__updateQuery):
            __temp: list = []
            for _ in keys:
                for object in collection['Data']:
                    if (TreleadbClient.__Validate__Where__Query__Lists__(list(_.values()), list(object.values()))):
                        for newK, newV in list(self.data.items()):
                            object[newK] = newV
                        object['updated_at'] = time.ctime()
                        __temp.append(object)
            
            with open(os.path.join(self.__dbPath, self.__dbName, f'{self.__collection}.json'), 'w') as _f:
                if (self.__secretKey == None):
                    _f.write(json.dumps(collection))
                else:
                    data = Fernet(self.__secretKey).encrypt(bytes(json.dumps(collection, default=str).encode('utf-8')))
                    _f.write(str(data.decode('utf-8')))
                _f.close()

            self.data.clear()
            self.data = __temp

        return self                 

        

    def insert(self, keys: dict) -> Self:
        if (not self.__collection):
            raise Exception (f"No Collesction Has Been Selected")
        
        collection = self.__ReadCollection__(self.__collection)
        
        dbSchema = list(collection['Schema'].keys())[:-3]
        dbSchemaDataTypes = list(collection['Schema'].values())[:-3]

        if (list(keys.keys()) != dbSchema):
            return self.__schema_Exception(keys, self.__active_Collection)
        for clientSchemaValuesType, dbSchemaValuesType in zip(list(keys.values()), dbSchemaDataTypes):
            if (type(clientSchemaValuesType).__name__ != dbSchemaValuesType):
                raise Exception (f"Invalid Schema '{keys}' For Collection '{self.__collection}' From Database '{self.__dbName}'.")
            
        keys['created_at'] = time.ctime()
        keys['updated_at'] = time.ctime()
        keys['__id'] = str(uuid.uuid4())
        collection['Data'].append(keys)

        with open(os.path.join(self.__dbPath, self.__dbName, f'{self.__collection}.json'), 'w') as _f:
            if (self.__secretKey == None):
                _f.write(json.dumps(collection))
            else:
                data = Fernet(self.__secretKey).encrypt(bytes(json.dumps(collection, default=str).encode('utf-8')))
                _f.write(str(data.decode('utf-8')))
            _f.close()

        self.__collection = None
        return keys



    def update(self, keys: dict) -> Self:
        if (not self.__collection):
            raise Exception (f"No Collesction Has Been Selected")
        
        collection = self.__ReadCollection__(self.__collection)

        if (not all(_ in list(collection['Schema'].keys()) for _ in list(keys.keys()))):
            raise Exception (f"Invalid Keys '{keys}' For Collection '{self.__collection}' In Database '{self.__dbName}'")
        
        

        self.__updateQuery = True
        self.__getQuery = False

        if (not len(keys)):
            self.data = collection['Data']
            return self
        
        updateKeys = list(keys.keys())
        if ('__id' in updateKeys or 'created_at' in updateKeys or 'updated_at' in updateKeys):
            raise Exception (f"Keys: ['__id', 'created_at', 'updated_at'] Are Only Read Mode For Client")
        
        self.data = keys
        return self
    


    def delete(self, *keys: dict, Full: bool = False) -> Self:
        if (not self.__collection):
            raise Exception (f"No Collesction Has Been Selected")
        if (not len(keys)):
            self.data = []
        
        collection = self.__ReadCollection__(self.__collection)

        for _ in keys:
            if (not all(_ in list(collection['Schema'].keys()) for _ in list(_.keys()))):
                raise Exception (f"Invalid Keys '{keys}' For Collection '{self.__collection}' In Database '{self.__dbName}'")
        
        if (Full):
            self.data = collection['Data']
            collection['Data'].clear()
        else:
            for _ in keys:
                for object in collection['Data']:
                    if (TreleadbClient.__Validate__Where__Query__Lists__(list(_.values()), list(object.values()))):
                        self.data.append(object)
                        collection['Data'].remove(object)

        with open(os.path.join(self.__dbPath, self.__dbName, f'{self.__collection}.json'), 'w') as _f:
            if (self.__secretKey == None):
                _f.write(json.dumps(collection))
            else:
                data = Fernet(self.__secretKey).encrypt(bytes(json.dumps(collection, default=str).encode('utf-8')))
                _f.write(str(data.decode('utf-8')))
            _f.close()
        
        return self