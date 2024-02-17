# TreleaDB

TreleaDB is a database, its provides object-oriented database for Python that provides a high-degree of transparency.

Its a very simple Database build for developing mini projects. It provides encryption, hashing and other specifications.

## Downloads

TreleaDB is distributed through the Python Package Index.

You can install the TreleaDB using pip command:

```
pip install treleadb
```

# Database Class

### __Database__ class provides methods for creating, connecting to a database and bonus schema rule validation and migration

__Constructor Parameters:__
- __dbName__ Database Name
- __dbPath__ Optional Datbase Path
- __secretKey__ Optional paraphrase for hashing and encryption

__classMethods__:
- __setupCollection(__ self, collName: str __)__
- __modelSchema(__ self, Schema: dict __)__
- __migrate(__ self, data: list = None __)__
- __dropDatabase(__ self __)__
- __dropCollection(__ self, collName: str __)__

### Creating a mini database with one collection.
```python
# migartion.py
from treleadb import Database
import json

# initialize object
mydb = Database(dbName="MyFirstDb")

# specify schema collection then setup full collection
todoSchema = { 'title': str, 'description': str }
todos = mydb.setupCollection("Todos").modelSchema(todoSchema).migrate()

# preview output
# all json info is in .data attribute
print(json.dumps(todos.data, indent=4))
```
```bash
# Run this command
python3 ./migration.py
```
```json
{
    "_Database": "MyFirstDb",
    "_DatabasePath": "/some_path/treleadb/MyFirstDb",
    "_Collection": "Todos",
    "_CollectionPath": "/some_path/treleadb/MyFirstDb/Todos.json",
    "_Encryption": false,
    "_Migration_created_at": "Sat Feb 17 19:05:29 2024",
    "_Migration_updated_at": "Sat Feb 17 19:05:29 2024",
    "Schema": {
        "title": "str",
        "description": "str",
        "created_at": "str",
        "updated_at": "str",
        "__id": "str"
    },
    "Data": []
}
```

### Lets develop more complex database (like a mini reddit clone) with encryption layer and data seeds on it.

```python
# migartion.py
from treleadb import Database
import datetime
from faker import Faker     # pip install Faker for seeding fake data
import json


# Optional Parameter For Encryption: secretKey: str = None
mydb = Database(dbName="RedditClone", secretKey="password_for_db")
fake = Faker()


# Generate 3 collections: Users, Posts, Comments

# ----------------------
# Setup Users Collection

userSchema: dict = { 
    'user_name': str,
    'user_email': str,
    'user_dateOfBirth': datetime.date,
    'user_password': str,
    'user_thumbnail': str,
    'user_isVerified': bool
}

userSeeds: list = list()
for _ in range(20):
    user: dict = dict()
    user['user_name'] = str(fake.first_name())
    user['user_email'] = str(fake.email())
    user['user_dateOfBirth'] = datetime.date(int(fake.year()), int(fake.month()), int(fake.random.randint(1, 30)))
    user['user_password'] = str(''.join(fake.words(nb = 2)))
    user['user_thumbnail'] = str(fake.uri())
    user['user_isVerified'] = bool(fake.boolean())
    userSeeds.append(user)

users = mydb.setupCollection('Users').modelSchema(userSchema).migrate(userSeeds)

# preview Users output
print(json.dumps(users.data, indent=4))


# ----------------------
# Setup Posts Collection

postSchema: dict = {
    'user_name': str,
    'post_title': str,
    'post_description': str,
    'post_thumbnail': str,
    'post_likes': list,
    'post_comments': int
}

postSeeds: list = list()
for _ in range(30):
    post: dict = dict()
    post['user_name'] = str(fake.first_name())
    post['post_title'] = str(" ".join(fake.words(nb = 2)))
    post['post_description'] = str(fake.text(max_nb_chars=1000))
    post['post_thumbnail'] = str(fake.uri())
    post['post_likes'] = list(fake.first_name() for _ in range(100))
    post['post_comments'] = int(fake.random.randint(1, 50))
    postSeeds.append(post)

posts = mydb.setupCollection('Posts').modelSchema(postSchema).migrate(postSeeds)

# preview Posts output
print(json.dumps(posts.data, indent=4))


# -------------------------
# Setup Comments Collection

commentSchema = {
    'post_id': str,
    'user_name': str,
    'comment_text': str
}

commentSeeds: list = list()
for _ in range(40):
    comment: dict = dict()
    comment['post_id'] = str(fake.uuid4())
    comment['user_name'] = str(fake.first_name())
    comment['comment_text'] = str(fake.text(max_nb_chars=100))
    commentSeeds.append(comment)

comments = mydb.setupCollection('Comments').modelSchema(commentSchema).migrate(commentSeeds)

# preview Comments output
print(json.dumps(comments.data, indent=4))
```
```bash
# Run this command
python3 ./migration.py
```
```json
{
    "_Database": "RedditClone",
    "_DatabasePath": "/some_path/treleadb/RedditClone",
    "_Collection": "Users",
    "_CollectionPath": "/some_path/treleadb/RedditClone/Users.json",
    "_Encryption": true,
    "_Migration_created_at": "Sat Feb 17 19:39:51 2024",
    "_Migration_updated_at": "Sat Feb 17 19:39:51 2024",
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
            "user_name": "Hannah",
            "user_email": "richardhill@example.org",
            "user_dateOfBirth": "2012-05-05",
            "user_password": "Americanstrategy",
            "user_thumbnail": "http://www.wallace-martin.org/tagfaq.php",
            "user_isVerified": true,
            "created_at": "Sat Feb 17 19:39:51 2024",
            "updated_at": "Sat Feb 17 19:39:51 2024",
            "__id": "14ae9626-02b6-4da5-8a60-1623162ee855"
        },
        {
            "user_name": "Jack",
            "user_email": "jonespatricia@example.org",
            "user_dateOfBirth": "2005-09-05",
            "user_password": "girlshake",
            "user_thumbnail": "http://wade.org/tagmain.html",
            "user_isVerified": false,
            "created_at": "Sat Feb 17 19:39:51 2024",
            "updated_at": "Sat Feb 17 19:39:51 2024",
            "__id": "9d5ed87d-2bc7-4975-bd3a-ab64884df6bd"
        },
        ...
    ]
}
{
    "_Database": "RedditClone",
    "_DatabasePath": "/some_path/treleadb/RedditClone",
    "_Collection": "Posts",
    "_CollectionPath": "/some_path/treleadb/RedditClone/Posts.json",
    "_Encryption": true,
    "_Migration_created_at": "Sat Feb 17 19:39:51 2024",
    "_Migration_updated_at": "Sat Feb 17 19:39:51 2024",
    "Schema": {
        "user_name": "str",
        "post_title": "str",
        "post_description": "str",
        "post_thumbnail": "str",
        "post_likes": "list",
        "post_comments": "int",
        "created_at": "str",
        "updated_at": "str",
        "__id": "str"
    },
    "Data": [
        {
            "user_name": "Thomas",
            "post_title": "final available",
            "post_description": "Six sing free natural hit itself despite big.\nHope talk through tree forward admit none modern. Both Republican participant particularly.\nCourse class business condition. Art forget media firm role. Agent popular head word.\nEverything at gas better raise. Opportunity speak place moment else sure national.\nBed produce author benefit gas nearly begin animal. Itself east knowledge.\nFeeling sing Mr big...",
            "post_thumbnail": "http://miller-wagner.com/categories/categoryprivacy.jsp",
            "post_likes": ["Karen", "Adam", "Laura", "Christopher", "Amber", ... ],
            "post_comments": 24,
            "created_at": "Sat Feb 17 19:39:51 2024",
            "updated_at": "Sat Feb 17 19:39:51 2024",
            "__id": "0614937c-7446-40e2-9f3b-6083d84e2f01"
        },
        {
            "user_name": "Erin",
            "post_title": "impact certainly",
            "post_description": "Realize notice central drug everything whether newspaper. Day democratic message material amount music politics.\nDevelopment subject mind treatment local market. Own general win act network worker student.\nRecognize movie that interesting. Staff page modern director expect support music.\nAgency field remember modern able call next. Past television real area forget call necessary...",
            "post_thumbnail": "https://levy-nelson.com/tag/main/blogregister.jsp",
            "post_likes": [ "Timothy", "Christopher", "Reginald", "Isaiah", "Allen", ... ],
            "post_comments": 2,
            "created_at": "Sat Feb 17 19:39:51 2024",
            "updated_at": "Sat Feb 17 19:39:51 2024",
            "__id": "b65e288b-7268-40b4-8449-0245ac9aab8d"
        }
        ...
    ]
}
{
    "_Database": "RedditClone",
    "_DatabasePath": "/some_path/treleadb/RedditClone",
    "_Collection": "Comments",
    "_CollectionPath": "/some_path/treleadb/RedditClone/Comments.json",
    "_Encryption": true,
    "_Migration_created_at": "Sat Feb 17 19:39:51 2024",
    "_Migration_updated_at": "Sat Feb 17 19:39:51 2024",
    "Schema": {
        "post_id": "str",
        "user_name": "str",
        "comment_text": "str",
        "created_at": "str",
        "updated_at": "str",
        "__id": "str"
    },
    "Data": [
        {
            "post_id": "014911d0-11f1-4beb-af3c-8e8b5c5d1265",
            "user_name": "Matthew",
            "comment_text": "Phone technology hope concern hit he special doctor. Institution international social glass such.",
            "created_at": "Sat Feb 17 19:39:51 2024",
            "updated_at": "Sat Feb 17 19:39:51 2024",
            "__id": "7e5afdbd-292a-418e-a388-336c2f551a5c"
        },
        {
            "post_id": "d0752977-49a4-4ece-9ef0-13a98da42150",
            "user_name": "Monica",
            "comment_text": "Method send process commercial arrive. Exist add south.",
            "created_at": "Sat Feb 17 19:39:51 2024",
            "updated_at": "Sat Feb 17 19:39:51 2024",
            "__id": "1c5d0851-a306-43ea-a4aa-7caf513f5007"
        },
        ...
    ]
}
```

### Analyzing Database Structure

```bash
# Run this command

$: tree <_DatabasePath Value>

/some_path/treleadb/RedditClone
├── Comments.json
├── Posts.json
└── Users.json

1 directory, 3 files
```

### Preview content from a collection file

```bash
# Run this command

$: cd <_DatabasePath Value>

$: cat Users.json

gAAAAABl0O9nepF6-e0nEKF_bkg9p_WUzxDLVhAsN_gFCjiifQMWJCQLZjs7K7xk-SMf_nzgIsnWnVx7Bl23_Ou_uG9ddjO7DBDJSl-nmZ-00DkLF99saAtI-zh2Yt_Q5mKClksdDQdi1umoZWkOlB54M8Lx_7pNak1hv1fCZw8iJu2k4DN0xgSlXKbhn1AAo6mh_cVYnfQga6sEf_I7lKpYZcAwQM3-cILajm97wKCindYVc36MkCCU1tqFXntED4w7eAT7lkrLFxgREZGFx30DOamLk4SqOupE3_TQ1YDSp69xzZPNfmq_9D7zBum4tkyDD6Qvb-n78FkIcZon5T-TX9wd9UmlGEohD_vT2tPELabcBPdul8rOt0KORi_52LAWedF1ORVAXtRCa_AWqE607pkra3b_2cv0xIA-QqixMvy071HVyH2xOAL-m5Oh4Rk0mrjx2WhT51vjlz1DGdb93wtRe5wwuWkICAtQmaAAkdP4NOTWzA1GaoyRU6Iepk-tx_Uaj8vrwdT5BlN79ipQpQqzJOx1prLBOpqtDIduOcJV6vQ8QL7sHEO0Ti8kDX0a-CScP2YhOyA4420JruJBAZYx5J_OAR6gOrH9eys0CN-16nHMUIn1GYehe2yHABScFPuoN6uyr2dp2r58LP5ouYv-XEFhb03dOS_E8_yZSphM834asW9jsf8PYRExE2yuY7HSd9F9CH-389jkhq-O3RLMRCM-136wpAjHuWeUpVBXgZ2imEVXJjbsAoUhjz6sD325PLuTwiDhDwdeng_SFK5Dqw5oUQ8-bIVuEMtjAjIOgpkJ-8uPpa74FLUWqd13DjXtwadsN3qsQJbqJFBq56xZ-nAebn3HnC0hrBF_ayIz8QToMAU4cDOJwfLxtTigS3lYOFmD5Zz2kQBieW1wItpFzLlvWoTflL5H5RphWz-KWwlR1S8NSXgN5oXSuVAFTK3y0y0oboCfZg615QjDhQDI0Q-U49TMEqqHyl7hHkw-Wdonx5eBKKoNNfiX_zuGeNdxw1iGqOjIuD9emDlRQj2W9LZC8b4oRFY3TKBIBJF5uMC9y8xIeXmznhWvjT9MTrAoIp7sYvHD_qA74DROF7T37UFU4-Cdt4KXpI8MKLhoAIRH0-S0H4LLhvglJJP2cApBQmTbYuIT8jdsxNWewNW3_lG7SL6KdlqcalTRrgJmgU_mkOi7hbde0HbnJbk6f-vuHfceFcGZLqmUlGNpBi6Tr9ySMpnW0X-Hu5qsu3C4Qn8lzoZSYQYzlw0RtDtlo-GBNJyS7uM91MUK45pFBCbWZ1TUi1ricNMTc4rGMgD8YXKH9G-ekwL0gcrgKJpTPaJoxI6wHNZTXbnWsHDUt1iPbCPmLN4tI_mv5I4iY6k3ZfoMr3zhWz4E5boo7NtPu1Qx-mSqyNseBQgbXln4SaqVuWe5NSdHyZ5glUzC5iFJebKa8Asi-7JzZDLb9hD_TCm2LI1ejWLnV94GNpBcmV01DMcZPnhwKCHFMlh128WbqLbn2HCbERYyG_uiSk8Kvbfkm7A4MmhjkZ1jHmKEGnCqA0NQ40J2U81TwbiOawjDq4PwpaPqwlDYVqMUztol4Lddk8crBnzKuzbsVXs5psi1a8f5uggTMSpPflUyo66mt4Oze1crO9Gh2FtcOLgh1ycQYhkkhQ1UWU5I-pjfHUdWGphJpRgXTJxMp7PS7oBWxo_s37oYSB6FZUBFOJa9-o6_c1ppJvpj0xG0qvtf4OmFE2qcgYs-deAcyCqxUTFGKYxTH2DCU_yrR_-wrNvZQDt-kidNu8SPFTc6gIZ29ogdt71cZUjaff14ViHdOnRWej4t2wuxqfK2hBxR7c9Pu4UmEMJk18KpBiqoC5fRs5Z5INC_ikRuJUt-RFvnV2zt2oLG-1KwSYuFFqHRa8LPdChnVcPIvuduySg7zmg5sV2l6tObhmCle-3y4MCMgChJFGYY5t8A0sfC79wOgtMJ0jWcw_DP0LhyU_A5Nebd9sohpm3LL7rdhU7j0nH9U6gE1V78zgmMNgMLPXgE2hIQ06WDvAAGgEAubOvZ-ZKzyxFpfnY-JR5lbCjFTeZtyxu0dHZ3mPvSVOrkZdytxov7fu5mi1X8FWd1rF_A8vMmslH1Ocn7szK0wk_tRqItyuEEAUOhzaNdVnhAMPxlmYoPeOW_dJiw_uDHjHFMexjHBqIdf3jSoOelB4iIHSphaT9W90Bn2qRHBT2YziGZPnQJW0F2yFkYYRfuOl7gffgkQaJ0eJsqcwnGor-XDv3xV77tW9KA6XeVFNgHPbJm5nUelvsJGCudOqCY_Z5Z4UE9Ekd22DcrpMhAQ5BgFIw9mxyHUkoRzskumqwrF1SrSjMhFA7hvPJTIf4CB_fXP19shRP30bHc4f72EKLolQYw7H-_DrlhxWpGzyEurDnzI3ClCTztrT7Ng7kZHVnelLODwYQyXCi_7v7BRNefIOzweuhTsiUTyAFE6fh6rBzdT-T1zizz0o23qtBjqbAgSHsstOxF2reMEbXt4pV6bwnXgB4hvCSVYcUobXeOSLp3Xoy5SsyQnYzjVU94pVrVJqiTIh2tCwMto0FB4ibEOqhURFA0exbR6aEMCzQDoB3v5PqnFuugptTT6k0ceq7_jXTvkn69tECH16pA7H5MAr_opgkfxW0pR2P8zBiyBAlLNiJWNnALBH0Cvdhc74sDWCnGaCKLNQWEnQDPiu-gCrL1w9y2mlw0QicsiTiFdnUdWc9WtrJxcCUdDfiS3-45QRDObXVU5foHfUAb_5a-xv2PP_UsUY7P-I1ciOJkF0iw9z8dRp9Hy1d0D_RUAdRGaSHTy74DydDWlmJK34OWad1b2-imOpzghujfqAbhXudaV50W1o4gBE4e5fJJVRS_ViPDYTAvfmCS9vUMyjCHNznWyW87T-TW1byn_h-jbUVFLqQfwv6m-V0Fw_6-UYo9DP4Dc7kMgzV0kzpugti79yAqLti6ZoeU0dQwlGD39r2_psFimmnl-wZF9KkZ8TcL3HJqsnfFXKQw1Sane303fdWQt9gJ_z-7wLlL058LANb1rqEGpdaizbih2BotWisOe9zC-c_TLe7VFzvTZMjVQuZWIApTaVEeBAjCttmyxEpmZwjGpC-6xmTD
```

### Drop Collections using .dropCollection() classMethod

```python
# drop.py
from treleadb import Database

# connect to an existent db
mydb = Database(dbName="RedditClone", secretKey="password_for_db")

# drop an existent collection
try:
    mydb.dropCollection("Comments")
    print("Collection Successfully Deleted")
except Exception as e:
    print(e)
```
```bash
# Lets run command drop.py

python3 ./drop.py

# Output Should Be:
# Collection Successfully Deleted
```
```bash
# Lets run another time command drop.py

python3 ./drop.py

# Output Should Be:
# Invalid Collection 'Comments' In Database 'RedditClone'
```

### Drop with wrong secretKey

```python
# modify secretKey parameter and dropCollection parameter in drop.py

# ...

mydb = Database(dbName="RedditClone", secretKey="wrong_pass")

# ...

mydb.dropCollection("Posts")

# ...
```
```bash
# Lets run another time command drop.py

python3 ./drop.py

# Output Should Be:
# Invalid Encrypted secretKey 'U7z0iZuP4pa4OdhUO3ZlB...' For Database 'RedditClone'
```
In conclusion the secretKey can be used like a security layer for your database and collections.
Best practice is to save the content of secretKey into a __.env__ file.

### Drop Database using .dropDatabase() classMethod

```python
# drop.py
from treleadb import Database

# connect to an existent db
mydb = Database(dbName="RedditClone", secretKey="password_for_db")

# drop an existent Database
try:
    mydb.dropDatabase()
    print("Database Successfully Deleted")
except Exception as e:
    print(e)
```
```bash
# Lets run command drop.py

python3 ./drop.py

# Output Should Be:
# Database Successfully Deleted
```
### Lets see if _DatabasePath still exists
```bash
# Run this command

$: tree <_DatabasePath Value>

<_DatabasePath Value>  [error opening dir]

0 directories, 0 files
``` 