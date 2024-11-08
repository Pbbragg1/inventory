from sqlalchemy import (create_engine, Column, Integer, String, Date)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class inventory(Base):
    __tablename__ = "inventory"

    prodeuct_id = Column(Integer, primary_key=True)
    product_name = Column("Product", String)
    product_quantity = Column("Quantity", Integer)
    product_price = Column("Price", Integer)
    date_updated = Column("Dade updated", Date)

    def __repr__(self):
        return f"ID: {self.product_id}, Name: {self.product_name}, Quantity: {self.product_quantity}, Price: {self.product_price}, Date: {self.date_updated}"
