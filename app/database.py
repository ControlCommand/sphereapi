from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:
    
#     try:
#         conn = psycopg2.connect(host='127.0.0.1', database='globalsphere', user='backend_tower', password= 'Khalafaland14#%', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connection Was Successful")
        
#         break
#     except Exception as error:
#         print("Connection to database failed")    
#         print("Error:", error)
#         time.sleep(2)
        """