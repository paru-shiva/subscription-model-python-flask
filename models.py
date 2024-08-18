from sqlalchemy import Column, Integer, String
from database import Base


class Customer(Base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String(50), unique=False)
    pan = Column(String(50), unique=True)

    def __init__(self, customer_name=None, pan=None):
        self.customer_name = customer_name
        self.pan = pan

    def __repr__(self):
        return f"{self.customer_id} {self.customer_name}"


class Product(Base):
    __tablename__ = "product"
    product_name = Column(String(50), primary_key=True)
    product_description = Column(String(50), unique=False)
    product_annual_cost = Column(Integer, unique=False)

    def __init__(
        self, product_name=None, product_description=None, product_annual_cost=None
    ):
        self.product_name = product_name
        self.product_description = product_description
        self.product_annual_cost = product_annual_cost

    def __repr__(self):
        return f"{self.product_name}"


class Subscription(Base):
    __tablename__ = "subscription"
    subscription_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, unique=False)
    product_name = Column(String(50), unique=False)
    start_date = Column(String(100), unique=False)
    end_date = Column(String(100), unique=False)
    no_of_subscriptions = Column(Integer, unique=False)

    def __init__(
        self,
        customer_id=None,
        product_name=None,
        start_date=None,
        end_date=None,
        no_of_subscriptions=None,
    ):
        self.product_name = product_name
        self.customer_id = customer_id
        self.start_date = start_date
        self.end_date = end_date
        self.no_of_subscriptions = no_of_subscriptions

    def __repr__(self):
        return f"{self.product_name} {self.customer_id} {self.start_date} {self.end_date} {self.no_of_subscriptions}"
