import platform
import os
import time
import json
from typing import Self
import uuid
import shutil

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class Database:

    def __init__(self, dbName: str, dbPath: str = None, secretKey: str = None) -> None:
        self.__secretKey = None
        self.__dbName: str = dbName
        self.__collection: str = None
        self.__data: dict = {}
        self.data: dict = {}
        
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
        if (not os.path.exists(self.__dbPath)):
            os.mkdir(self.__dbPath)



    def __Verify__SecretKey__On__Collection__Drop__(self, collName: str) -> bool:
        if (self.__secretKey == None):
            self.__secretKey = ""

        with open(os.path.join(self.__dbPath, self.__dbName, f'{collName}.json'), 'r') as _f:
            try:
                Fernet(self.__secretKey).decrypt(_f.read().encode('utf-8'))
                _f.close()
                return True
            except:
                return False




    def setupCollection(self, collName: str) -> Self:
        self.__collection = collName
        return self
    


    def modelSchema(self, Schema: dict) -> Self:
        if (self.__collection == None):
            raise Exception (f"Someting Went Wrong Into Your Chaining Method")
        
        self.__data['_Database'] = self.__dbName
        self.__data['_DatabasePath'] = os.path.join(self.__dbPath, self.__dbName) 
        self.__data['_Collection'] =  self.__collection
        self.__data['_CollectionPath'] = os.path.join(self.__dbPath, self.__dbName, f'{self.__collection}.json')
        self.__data['_Encryption'] = True if self.__secretKey != None else False
        self.__data['_Migration_created_at'] = time.ctime()
        self.__data['_Migration_updated_at'] = time.ctime()

        self.__data['Schema'] = {}
        self.__data['Data']   = []

        Schema['created_at'] = str
        Schema['updated_at'] = str
        Schema['__id']       = str

        for key, val in Schema.items():
            self.__data['Schema'][key] = val.__name__
        return self
    


    def migrate(self, data: list = None) -> Self:
        if (not os.path.exists(os.path.join(self.__dbPath, self.__dbName))):
            os.mkdir(os.path.join(self.__dbPath, self.__dbName))

        if (self.__collection == None and bool(self.__data)):
            raise Exception (f"Alert From Migration Process: 'collection={self.__collection}' And 'data={self.__data}'. Migartion Failed To Create Collection '{self.__collection}' In Database '{self.__dbName}'.")
        
        if data:
            for _ in data:
                if (_ and list(_.keys()) != list(self.__data['Schema'].keys())[:-3]):
                    raise Exception (f"Invalid Schema '{_}' For Migration")
                
                dataValuesTypes = [type(i).__name__ for i in _.values()]
                schemaValuesTypes = [j for j in self.__data['Schema'].values()]

                if (dataValuesTypes != schemaValuesTypes[:-3]):
                    print(dataValuesTypes)
                    print(schemaValuesTypes[:-3])
                    raise Exception (f"Invalid Schema '{_}' For Migration")
                
                _['created_at'] = time.ctime()
                _['updated_at'] = time.ctime()
                _['__id'] = str(uuid.uuid4())
                self.__data['Data'].append(_)

        self.data = self.__data
        if (self.__secretKey):
            fernet = Fernet(self.__secretKey)
            self.__data = fernet.encrypt(bytes(json.dumps(self.__data, default=str).encode('utf-8')))
            
        with open(os.path.join(self.__dbPath, self.__dbName, f'{self.__collection}.json'), 'w') as _f:
            if (type(self.__data).__name__ == 'bytes'):
                _f.write((self.__data).decode('utf-8'))
            else:
                _f.write(str(self.__data))
            _f.close()

        self.__collection = None
        self.__data = {}
        return self



    def dropDatabase(self) -> int:
        if (not os.path.exists(os.path.join(self.__dbPath, self.__dbName))):
            raise Exception (f"Invalid Database '{self.__dbName}'")
        
        if (self.__Verify__SecretKey__On__Collection__Drop__(os.listdir(os.path.join(self.__dbPath, self.__dbName))[0].replace('.json', ''))):
            shutil.rmtree(os.path.join(self.__dbPath, self.__dbName), ignore_errors=True)
            return 1
        else:
            raise Exception (f"Invalid Encrypted secretKey '{str(self.__secretKey.decode('utf-8'))}' For Database '{self.__dbName}'")
        


    def dropCollection(self, collName: str) -> int:
        if (not os.path.exists(os.path.join(self.__dbPath, self.__dbName, f'{collName}.json'))):
            raise Exception (f"Invalid Collection '{collName}' In Database '{self.__dbName}'")
        
        if (self.__Verify__SecretKey__On__Collection__Drop__(collName)):
            os.remove(os.path.join(self.__dbPath, self.__dbName, f'{collName}.json'))
            return 1
        else:
            raise Exception (f"Invalid Encrypted secretKey '{str(self.__secretKey.decode('utf-8'))}' For Database '{self.__dbName}'")