from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "sqlite:///movies.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)

# Define a test model
class TestModel(Base):
    __tablename__ = "test_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Create the database
Base.metadata.create_all(engine)
print("Database and table created successfully!")

# Insert a record
Session = sessionmaker(bind=engine)
session = Session()
test_record = TestModel(name="Test Name")
session.add(test_record)
session.commit()
print("Record inserted successfully!")
