import os

basedir = os.path.abspath(os.path.dirname(__file__))
use_local_database = False

class Config:
    if use_local_database:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")
    else:
        DB_USER=os.environ.get("DB_USER")
        DB_PW=os.environ.get("DB_PW")
        DB_URL=os.environ.get("DB_URL")
        DB_DB=os.environ.get("DB_DB")   
        DB_PROJECT_ID=os.environ.get("DB_PROJECT_ID") 
        DB_INSTANCE_NAME=os.environ.get("DB_INSTANCE_NAME")
        
        DB_URL = 'postgresql+psycopg2://root:'+DB_PW+'@'+DB_URL+'/'+DB_DB+'?host=/cloudsql/'+DB_PROJECT_ID+':'+DB_INSTANCE_NAME
        # DB_URL = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(user=DB_USER,pw=DB_PW,url=DB_URL,db=DB_DB)
        # DB_URL=postgres://user:password@/dbname?host=/path/to/db

        SQLALCHEMY_DATABASE_URI = DB_URL

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get("TRACK_MODS")



