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
