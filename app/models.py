import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import db_path

# SQLAlchemy setup
DATABASE_URL = f"sqlite:///{db_path}"
engine = sql.create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Accounts model
class Account(Base):
    __tablename__ = "accounts"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    name = sql.Column(sql.String, nullable=False, unique=True)
    bank_name = sql.Column(sql.String, nullable=False)
    account_type = sql.Column(sql.String, nullable=False)  # e.g., 'Checking', 'Credit Card', 'Investment'

    def __repr__(self):
        return f"<Account(name={self.name}, bank={self.bank_name}, type={self.account_type})>"

class AccountBalance(Base):
    __tablename__ = "account_balances"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    account_id = sql.Column(sql.Integer, sql.ForeignKey("accounts.id"), nullable=False)
    date = sql.Column(sql.Date, nullable=False)
    balance = sql.Column(sql.Float, nullable=False)

    def __repr__(self):
        return f"<AccountBalance(account_id={self.account_id}, date={self.date}, balance={self.balance})>"
    
class Transaction(Base):
    __tablename__ = "transactions"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    account_id = sql.Column(sql.Integer, sql.ForeignKey("accounts.id"), nullable=False)
    date = sql.Column(sql.Date, nullable=False)
    amount = sql.Column(sql.Float, nullable=False)
    category = sql.Column(sql.String, nullable=False)  # e.g., 'Groceries', 'Rent', 'Salary'
    description = sql.Column(sql.String, nullable=True)

    def __repr__(self):
        return f"<Transaction(account_id={self.account_id}, date={self.date}, amount={self.amount}, category={self.category})>"

class Budget(Base):
    __tablename__ = "budgets"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    category = sql.Column(sql.String, nullable=False, unique=True)  # e.g., 'Groceries', 'Rent', 'Entertainment'
    amount = sql.Column(sql.Float, nullable=False)  # Planned budget for the category

    def __repr__(self):
        return f"<Budget(category={self.category}, amount={self.amount})>"

class NetWorth(Base):
    __tablename__ = "net_worth"

    id = sql.Column(sql.Integer, primary_key=True, autoincrement=True)
    date = sql.Column(sql.Date, nullable=False, unique=True)  # Unique snapshot per date
    total_assets = sql.Column(sql.Float, nullable=False)
    total_liabilities = sql.Column(sql.Float, nullable=False)
    net_worth = sql.Column(sql.Float, nullable=False)

    def __repr__(self):
        return f"<NetWorth(date={self.date}, net_worth={self.net_worth})>"

