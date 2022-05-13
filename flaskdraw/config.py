import os
import urllib.parse 


basedir = os.path.abspath(os.path.dirname(__file__))
use_local_database = True

class Config:
    if use_local_database:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")
    else:
        POSTGRES_URL = os.environ.get("PUBLIC_IP_ADDRESS")
        POSTGRES_USER = os.environ.get("POSTGRES_USER")
        POSTGRES_PW = os.environ.get("POSTGRES_PW")
        POSTGRES_DB = os.environ.get("POSTGRES_DB")
        
        DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
        SQLALCHEMY_DATABASE_URI=DB_URL

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get("TRACK_MODS")

