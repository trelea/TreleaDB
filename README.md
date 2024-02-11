# TreleaDB

TreleaDB is a database, its provides object-oriented database for Python that provides a high-degree of transparency.

Its a very simple Database build for developing mini projects. It provides encryption and hashing and other specifications.

## Downloads

TreleaDB is distributed through the Python Package Index.

You can install the TreleaDB using pip command:

```
pip install treleadb
```

## Examples

### __Database__ class provides methods to create and connect to a databases and create and migrate schemas and collections.

__Constructor Parameters:__
- __dbName__ Database Name
- __dbPath__ Optional Datbase Path
- __secretKey__ Optional paraphrase for hashing and encryption


Here is a basic example of creating a database with collection then setting up schema and migrate data.
First Step is to create a __migration.py__ file
```python
# migartion.py

# Import class Database for setup Db
from treleadb import Database

myDb = Database(dbName="NewApp")

# Defining Schema
userSchema = {
    'name': str,
    'email': str,
    'age': int
    # ... More details about user ...
}

# Migration Method Chaining Please !!!
users = myDb.setupCollection('Users').modelSchema(userSchema).migrate()
```


How to preview migration response from __classMethod__ __.migrate()__
```python
import json

# .data is atributte from the instance of class 
print(json.dumps(users.data, indent=4))
```


## Example of Migration Output Response
```json
{
    "_Database": "NewApp",
    "_DatabasePath": "/home/treleadev/treleadb/NewApp",
    "_Collection": "Users",
    "_CollectionPath": "/home/treleadev/treleadb/NewApp/Users.json",
    "_Encryption": false,
    "_Migration_created_at": "Thu Feb  8 23:00:07 2024",
    "_Migration_updated_at": "Thu Feb  8 23:00:07 2024",
    "Schema": {
        "name": "str",
        "email": "str",
        "age": "int",
        "created_at": "str",
        "updated_at": "str",
        "__id": "str"
    },
    "Data": []
}
```

## migrate() method

### migrate() method is the core of creating and setting data in database collections. This method can take optional list as a parameter to set data automatically on migration. 

### The migrate() method will reset and upgrade the entire collection if some changes were applied to schema. 

Here is an example using .migrate() to insert automatically data.

```python
# migartion.py

# Import class Database for setup Db
from treleadb import Database
import json

myDb = Database(dbName="NewApp")

# Defining Schema
userSchema = {
    'name': str,
    'email': str,
    'age': int
    # ... More details about user ...
}

# Migration Method Chaining Please !!!
users = myDb.setupCollection('Users').modelSchema(userSchema).migrate([
    {
        'name': 'John',
        'email': 'john_peter@mail.net',
        'age': 34
    },
    {
        'name': 'Ann',
        'email': 'annmyce12@nmail.net',
        'age': 19
    },
    {
        'name': 'Nick',
        'email': 'holdernick222@gmail.com',
        'age': 21
    }
    # More Data ...
])

print(json.dumps(users.data, indent=4))
```

The Expected Result Of Migration.
```json
{
    "_Database": "NewApp",
    "_DatabasePath": "/home/treleadev/treleadb/NewApp",
    "_Collection": "Users",
    "_CollectionPath": "/home/treleadev/treleadb/NewApp/Users.json",
    "_Encryption": false,
    "_Migration_created_at": "Thu Feb  8 23:19:24 2024",
    "_Migration_updated_at": "Thu Feb  8 23:19:24 2024",
    "Schema": {
        "name": "str",
        "email": "str",
        "age": "int",
        "created_at": "str",
        "updated_at": "str",
        "__id": "str"
    },
    "Data": [
        {
            "name": "John",
            "email": "john_peter@mail.net",
            "age": 34,
            "created_at": "Thu Feb  8 23:19:24 2024",
            "updated_at": "Thu Feb  8 23:19:24 2024",
            "__id": "838c142b-ea7b-411c-9dd4-190b3bd992b0"
        },
        {
            "name": "Ann",
            "email": "annmyce12@nmail.net",
            "age": 19,
            "created_at": "Thu Feb  8 23:19:24 2024",
            "updated_at": "Thu Feb  8 23:19:24 2024",
            "__id": "8a4a6a88-d0f9-4e6c-9309-dc38a89c20c3"
        },
        { "more": "..." }
    ]
}
```
## What is secretKey parameter ?

### __secretKey__ parameter from constructor is a parameter that has the role of encrypting the collections. Is like a password for accesing database collections.

Here Is An Example Uisng secretKey.

```python
from treleadb import Database
import json

myDb = Database(dbName="NewApp", secretKey="mySecretKey_poiuytrewq1234")

# Defining Schema
userSchema = {
    'name': str,
    'email': str,
    'age': int
    # ... More details about user ...
}

# Migration Method Chaining Please !!!
users = myDb.setupCollection('Users').modelSchema(userSchema).migrate([
    {
        'name': 'John',
        'email': 'john_peter@mail.net',
        'age': 34
    },
    {
        'name': 'Ann',
        'email': 'annmyce12@nmail.net',
        'age': 19
    },
    {
        'name': 'Nick',
        'email': 'holdernick222@gmail.com',
        'age': 21
    }
    # More Data ...
])

print(json.dumps(users.data, indent=4))
```

Expected Output Result From A Migration With Encryption Key.

```json
{
    "_Database": "NewApp",
    "_DatabasePath": "/home/treleadev/treleadb/NewApp",
    "_Collection": "Users",
    "_CollectionPath": "/home/treleadev/treleadb/NewApp/Users.json",
    "_Encryption": true,
    "_Migration_created_at": "Thu Feb  8 23:24:05 2024",
    "_Migration_updated_at": "Thu Feb  8 23:24:05 2024",
    "Schema": {
        "name": "str",
        "email": "str",
        "age": "int",
        "created_at": "str",
        "updated_at": "str",
        "__id": "str"
    },
    "Data": [
        {
            "name": "John",
            "email": "john_peter@mail.net",
            "age": 34,
            "created_at": "Thu Feb  8 23:24:05 2024",
            "updated_at": "Thu Feb  8 23:24:05 2024",
            "__id": "09051f6b-d0e4-48f9-80cb-ded42968d2c9"
        },
        { "more": "..." }
    ]
}
```

Lets look at the content of file after using a secretKey

```text
//  ./NewApp/Users.json

gAAAAABlxUhZD48c31B4dn50QmsqRO6RVCA7F-yKChgwxEr_EFLAZ-umXU1UZdekJtDjBMhsz
TyRYvR56uCDeE2Npn5t0wzomu347CjsS4E7yKDCgqebYKKibSNoGjZ3o7_LarhX7n3aB83JOt
-rcnMCg_V9arW-N6yRfSa8uCKv7EHys0KDSBX7gnsz7jDZbv0F0cC-z0rD3Vu4sY3fmigNT1l
jl4TVYsc5PO0NrzxTTpVPhKAvdWTQXfh-QI5zqRLsFHdxgxP2rCnY0IGxSeylHG4TX0VxmjHZ
ujqoYJC-Fqzm9wO3sv2mL5PnmYoC16IVSHra0q3l3OfJ8QW--jLiHiuhhvH5727NovQQL3tog
B5W6DTN22Yebt0RaTlcVYi0gTmr21LpxPp8akVSVtMQb3yw_p-i_M6l-aB2nzd1G1_zS7cczq
mrmk4u0V9yg7u3zJIVsfnoYaNgHYWgRE8a746umVp5fVy4cGwbXjgmBfpdl0fvxSGYe8isPty
BnQX91krEukwGpwLDtbncSVW5qOMe8dtiHQZ8ph_6TzGFdC9K0Fq06KL0NGVqSYKl2AlF3LNq
ZQFT5BXkpticcS_YmA870n1dHBxbR7VcTaogrPGNLRNBwl2sjDYg1JNP78xjYw3xSuyVur-Cy
7QbpIZVhSAJ8hEHycIH-vNWsSWXzQIfmeK1g6XZyHHWxtI2eN_VozTqgeXMadqFoQnDdv46X_
Y-eGNQ3IYb4RFOM7L2BJ1srQMA62awLIRsBWw1q0yCmR5m5wKRKsEM0fbH_NbS3vYZ3ekhG_o
mWl3qw5uOLxFvJ6ERxq5rjY4koQu0zlru7-YDSG-YeRQ8q4zTYC9Ia-tduUSs13PLeuOZ9fSQ
XK-bSEk3HGVI2bO6vSSYp7qOVtEcvcPImBrgeHM015REN-NfS7eBnF0nY4JqB3tn1DWrWrWNJ
7V-fn_XaoMd2zALRaz7mWUewB0Al6ktfFOWBu3nBvjTw828XkfpgayDxWXDM0IyOH1fvqYA_F
o4Q6pZQFm8h4jvV-5m44WRbNU1GbO-LmIepolfeu_j3hZxsRUbpl4JEWUoUoTgwADVeoonM1e
FVCO466T_bcpxspMbGTvsr35nUDeAnXpQurkgmq4jNkOk_sV8t9WqdDG6QvhXYIMfwrhK1kVu
...
```

## TreleaDB Client
### TreleadbClient is a class that provides the general queries for database manipulation. Must use TreleadbClient only for CRUD operations.

### If you want to create, migarte, or drop somthing then you must use Database class.

Here is a full example for using TreleadbClient with Database.

```python
# migration.py file
from treleadb import Database
from datetime import date

myDb = Database(dbName="RedditClone", secretKey="qwerty")

# Users Collection
myDb.setupCollection('Users').modelSchema({
    'user_name': str,
    'user_email': str,
    'user_dateOfBirth': date,
    'user_password': str,
    'user_thumbnail': str,
    'user_isVerified': bool
}).migrate()

# Posts Collection
myDb.setupCollection('Posts').modelSchema({
    'user_name': str,
    'post_title': str,
    'post_description': str,
    'post_thumbnail': str,
    'post_likes': list,
    'post_comments': int
}).migrate()

# Comments Collection
myDb.setupCollection('Comments').modelSchema({
    'post_id': str,
    'user_name': str,
    'comment_text': str
}).migrate()
```
Run this command in terminal.
```bash
python3 ./migration.py
```

Lets see if collections were created using TreleadbClient class.

```python
# client.py
from treleadb import TreleadbClient
import json

# Very Important !!! If you used a secretKey on migration you also need to use it on client side.
db = TreleadbClient(dbName="RedditClone", secretKey="qwerty")

# classMethod -> getCollections() -> get all collections from specific database.
collections = db.getCollections()
print("Collections: ", collections)

# classMethod -> getCollection(collName: str, Schema: bool = False) -> get a collection...

# If second parameter 'Schema' is True then getCollection() will return the data plus collection Schema.

users_collection = db.getCollection('Users')
print("Users Collection: ", json.dumps(users_collection, indent=4))

users_collection = db.getCollection('Users', Schema=True)
print("Users Collection Schema True: ",json.dumps(users_collection, indent=4))
```
Run this command in terminal.
```bash
python3 ./client.py
```
Lets Preview output.
```text
Collections:  ['Posts.json', 'Users.json', 'Comments.json']

Users Collection:  []

Users Collection Schema True:  {
    "_Database": "RedditClone",
    "_DatabasePath": "/home/treleadev/treleadb/RedditClone",
    "_Collection": "Users",
    "_CollectionPath": "/home/treleadev/treleadb/RedditClone/Users.json",
    "_Encryption": true,
    "_Migration_created_at": "Fri Feb  9 21:04:16 2024",
    "_Migration_updated_at": "Fri Feb  9 21:04:16 2024",
    "Schema": {
        "user_name": "str",
        "user_email": "str",
        "user_dateOfBirth": "datetime",
        "user_password": "str",
        "user_thumbnail": "str",
        "user_isVerified": "bool",
        "created_at": "str",
        "updated_at": "str",
        "__id": "str"
    },
    "Data": []
}
```

## Insert Data Using TreleadbClient

### You can insert data into a specific collection using TreleadbClient queries.

Here is an example of inserting data in collection Users.

```python
# client.py
from treleadb import TreleadbClient
import datetime
import json

db = TreleadbClient(dbName="RedditClone", secretKey="qwerty")

# Very Important !!! Respect the Schema Rule
# Lets insert two user objects in Users collection
db.select('Users').insert({
    'user_name': 'miguel',
    'user_email': 'miguel_ann@dotnet.net',
    'user_dateOfBirth': datetime.date(2000, 12, 10),
    'user_password': 'koniciua_1234',
    'user_thumbnail': 'url_path_thumb.jpg',
    'user_isVerified': True
})
db.select('Users').insert({
    'user_name': 'angela',
    'user_email': 'angela_simone12@gmail.roro',
    'user_dateOfBirth': datetime.date(2005, 3, 20),
    'user_password': 'angelaKeyword',
    'user_thumbnail': 'url_path_thumb.jpg',
    'user_isVerified': False
})

# Because of method chaining prinicple you can also write like this:
# db.select('Users').insert({ ... }).insert({ ... }).insert({ ... })... 

# Output
users_data = db.getCollection('Users', Schema=True)
print(json.dumps(users_data, indent=4))
```
Run this command in terminal.
```bash
python3 ./client.py
```
Lets see the result in terminal.
```json
{
    "_Database": "RedditClone",
    "_DatabasePath": "/home/treleadev/treleadb/RedditClone",
    "_Collection": "Users",
    "_CollectionPath": "/home/treleadev/treleadb/RedditClone/Users.json",
    "_Encryption": true,
    "_Migration_created_at": "Fri Feb  9 21:39:44 2024",
    "_Migration_updated_at": "Fri Feb  9 21:39:44 2024",
    "Schema": {
        "user_name": "str",
        "user_email": "str",
        "user_dateOfBirth": "date",
        "user_password": "str",
        "user_thumbnail": "str",
        "user_isVerified": "bool",
        "created_at": "str",
        "updated_at": "str",
        "__id": "str"
    },
    "Data": [
        {
            "user_name": "miguel",
            "user_email": "miguel_ann@dotnet.net",
            "user_dateOfBirth": "2000-12-10",
            "user_password": "koniciua_1234",
            "user_thumbnail": "url_path_thumb.jpg",
            "user_isVerified": true,
            "created_at": "Fri Feb  9 21:39:45 2024",
            "updated_at": "Fri Feb  9 21:39:45 2024",
            "__id": "f3139a92-e65f-4a3f-8075-24830dd66afa"
        },
        {
            "user_name": "angela",
            "user_email": "angela_simone12@gmail.roro",
            "user_dateOfBirth": "2005-03-20",
            "user_password": "angelaKeyword",
            "user_thumbnail": "url_path_thumb.jpg",
            "user_isVerified": false,
            "created_at": "Fri Feb  9 21:39:45 2024",
            "updated_at": "Fri Feb  9 21:39:45 2024",
            "__id": "a2eff607-76e9-4cc5-80b2-53fbe0a42178"
        }
    ]
}
```

Lets check the content of Users collection.
```bash
cat ~/treleadb/RedditClone/Users.json

gAAAAABlxn-Bg_IjtJ62NlhnJOJNjgSg4QZtS8_dPkMgAwMJEIGzR01WSlIb6J39PSAySfWpbKHk9Ys_mg381gGufoxSWxBqbd-rFloxcKpJAfm5wLb561CXAptY2iAOAqX3fqtWtuiO13RNnsoeA9teref4P7MB2zHbd6tXz1imAInMhpmKjH-MhPV-GCKvNyruNNn8-pno_7so3Pei3SG3fiwc-XsNdj0nis8LbYbVn4M9b-6ng1gy0seYPilcW-X5bDKEcbqrtubVrgY8c3L94TrW1rG1Z0Nj38mvFDndwk4AUrNlr-KAPYHroo8C6-PbJLTJ6VOeQLGksNXSY5SaJpL6x-n7TnDavz5j-WhlFAWp9P9ZPQKkCi9C55JG6QABIebom7KNUkVfUCkJgcRrxiRRqaKQr5RzTp4IP7xK0qi55PZ_XjQVVYPOqgzh-HcxF7PBPY8MIOoP6HtEzsakNZjZvXcNrjfs9VUCeuKzk31ZuXUvb6yCUmfAYXQBA7wc0A9MhTkQTtHwYSDEREu-xrdkYdSGWjzEE1bE28cRgJkN_bqOc5HYEBzOoV0XHxVF09P6iCyZfo4Ds6m9g-pJmhbTbx1-Z5eHQntBF0ZTlxtHpNlGFyn3TO4XIKufAeYEtA2JTxLVV4QvCVKgdH03-0u2_1tFDknQsRuBro0cVTdqFxAamVnSJAx-BUSvHBOiRztu2iZclv-TP0L3lNew9M1NVMfn2563vTC59YGxNELp1rmImCPqHAbNru_ww9hcpD0VR1ECxTGq_cBStJYUfC2wJAO3BgQ1-Mm7mgc5WGaoXVr6ZVvsl43CT2QxYyOn8SPM
...
```

## TreleadbClient CRUD Methods

### TreleadbClient Class has the most used methods for CRUD operations on collections. Principle of using methods is very simple, methods are based on method chainin, and also can have some vulnerabilities so you must use this methods like in my documentation :)

### Getters Methods:
- __select(__ self, collName: str __)__
- __get(__ self, **keys: boll __)__
- __getCollection(__ self, collName: str, Schema: bool = False __)__
- __getCollections(__ self __)__
- __where(__ self, *keys: dict __)__

### Modifiers Methods:
- __insert(__ self, keys: dict __)__
- __update(__ self, keys: dict __)__
- __delete(__ self, keys: dict, Full: bool = False __)__

### In future will be implemented more methods, this project is in stage of developing. 