import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


connection = os.environ.get("CONNECTION", "mysql://root:@localhost/pokemontcgdb")
engine = create_engine(connection)

Session = sessionmaker(bind=engine)
#session = Session()

Base = declarative_base()

def initDb():
    Base.metadata.create_all(engine)
