from sqlalchemy.orm import Session
import app.models as models

def calculate_net_worth(session: Session, date):
    """
    Calculates total assets, total liabilities, and net worth for a given date.

    Parameters:
        session (Session): Active database session.
        date (date): The date for which to calculate net worth.

    Returns:
        tuple: (total_assets, total_liabilities, net_worth) as floats.
    """
    balances = session.query(models.AccountBalance).filter_by(date=date).all()
    
    total_assets = sum(b.balance for b in balances if b.balance > 0)
    total_liabilities = sum(abs(b.balance) for b in balances if b.balance < 0)
    net_worth = total_assets - total_liabilities  

    return total_assets, total_liabilities, net_worth

def add_net_worth_entry(session: Session, date):
    """
    Fetches balances, calculates net worth, and inserts a new NetWorth entry.

    Parameters:
        session (Session): Active database session.
        date (date): The date for which to store net worth.

    Returns:
        NetWorth: The newly created NetWorth entry.
    """
    total_assets, total_liabilities, net_worth = calculate_net_worth(session, date)

    new_entry = models.NetWorth(
        date=date,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        net_worth=net_worth
    )

    session.add(new_entry)
    session.commit()
    return new_entry

def add_account(session: Session, name: str, bank_name: str, account_type: str):
    """
    Adds a new account to the database.

    Parameters:
        session (Session): Active database session.
        name (str): The name of the account.
        bank_name (str): The bank or institution associated with the account.
        account_type (str): The type of account (e.g., 'Checking', 'Credit Card').

    Returns:
        Account: The newly created Account entry.
    """
    new_account = models.Account(name=name, bank_name=bank_name, account_type=account_type)
    session.add(new_account)
    session.commit()
    return new_account

def get_accounts(session: Session):
    """
    Retrieves all accounts from the database.

    Parameters:
        session (Session): Active database session.

    Returns:
        list: A list of Account objects.
    """
    return session.query(models.Account).all()

def delete_account(session: Session, account_id: int):
    """
    Deletes an account by ID.

    Parameters:
        session (Session): Active database session.
        account_id (int): The ID of the account to delete.

    Returns:
        bool: True if the account was deleted, False if not found.
    """
    account = session.query(models.Account).filter_by(id=account_id).first()
    if account:
        session.delete(account)
        session.commit()
        return True
    return False 

def update_balance(session: Session, account_id: int, date, balance: float):
    """
    Records a new balance entry for an account.

    Parameters:
        session (Session): Active database session.
        account_id (int): The ID of the account to update.
        date (date): The date of the balance entry.
        balance (float): The account balance on the given date.

    Returns:
        AccountBalance: The newly created balance entry.
    """
    balance_entry = models.AccountBalance(account_id=account_id, date=date, balance=balance)
    session.add(balance_entry)
    session.commit()
    return balance_entry

def get_balance(session: Session, account_id: int, date):
    """
    Gets the balance of an account for a specific date.

    Parameters:
        session (Session): Active database session.
        account_id (int): The ID of the account.
        date (date): The date for which to retrieve the balance.

    Returns:
        AccountBalance: The balance entry if found, else None.
    """
    return session.query(models.AccountBalance).filter_by(account_id=account_id, date=date).first()

def add_transaction(session: Session, account_id: int, date, amount: float, category: str, description: str = None):
    """
    Adds a transaction to the database.

    Parameters:
        session (Session): Active database session.
        account_id (int): The ID of the account the transaction is linked to.
        date (date): The transaction date.
        amount (float): The transaction amount.
        category (str): The category of the transaction (e.g., 'Groceries', 'Rent').
        description (str, optional): Additional details about the transaction.

    Returns:
        Transaction: The newly created transaction entry.
    """
    new_transaction = models.Transaction(
        account_id=account_id,
        date=date,
        amount=amount,
        category=category,
        description=description
    )
    session.add(new_transaction)
    session.commit()
    return new_transaction

def get_transactions(session: Session, account_id: int = None, start_date=None, end_date=None):
    """
    Fetches transactions, optionally filtered by account and date range.

    Parameters:
        session (Session): Active database session.
        account_id (int, optional): The ID of the account to filter by.
        start_date (date, optional): The start date for filtering transactions.
        end_date (date, optional): The end date for filtering transactions.

    Returns:
        list: A list of Transaction objects matching the criteria.
    """
    query = session.query(models.Transaction)
    
    if account_id:
        query = query.filter(models.Transaction.account_id == account_id)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    
    return query.all()
