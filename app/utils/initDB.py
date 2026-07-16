#import Base
from ..core.db import Base,engine
#import all db models
from ..database.models.user import User

def create_tables():
    Base.metadata.create_all(bind=engine)