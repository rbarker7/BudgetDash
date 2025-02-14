from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import app.models as models
from app.logger import logger  # Import the existing logger

def calculate_net_worth(session: Session, date):
    """
    Calculates total assets, total liabilities, and net worth for a given date.

    Parameters:
        session (Session): Active database session.
        date (date): The date for which to calculate net worth.

    Returns:
        tuple: (total_assets, total_liabilities, net_worth) as floats.
    """
    try:
        balances = session.query(models.AccountBalance).filter_by(date=date).all()

        total_assets = sum(b.balance for b in balances if b.balance > 0)
        total_liabilities = sum(abs(b.balance) for b in balances if b.balance < 0)
        net_worth = total_assets - total_liabilities  

        logger.debug(f"Net worth calculated for {date}: Assets={total_assets}, Liabilities={total_liabilities}, Net Worth={net_worth}")

        return total_assets, total_liabilities, net_worth
    except SQLAlchemyError as e:
        logger.error(f"Failed to calculate net worth for {date}: {e}", exc_info=True)
        raise

def add_net_worth_entry(session: Session, date):
    """
    Fetches balances, calculates net worth, and inserts a new NetWorth entry.

    Parameters:
        session (Session): Active database session.
        date (date): The date for which to store net worth.

    Returns:
        NetWorth: The newly created NetWorth entry.
    """
    try:
        total_assets, total_liabilities, net_worth = calculate_net_worth(session, date)

        new_entry = models.NetWorth(
            date=date,
            total_assets=total_assets,
            total_liabilities=total_liabilities,
            net_worth=net_worth
        )

        session.add(new_entry)
        session.commit()

        logger.debug(f"Net worth entry added for {date}")

        return new_entry
    except SQLAlchemyError as e:
        logger.error(f"Failed to add net worth entry for {date}: {e}", exc_info=True)
        session.rollback()
        raise

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
    try:
        new_account = models.Account(name=name, bank_name=bank_name, account_type=account_type)
        session.add(new_account)
        session.commit()

        logger.debug(f"Account '{name}' added (Bank: {bank_name}, Type: {account_type})")

        return new_account
    except SQLAlchemyError as e:
        logger.error(f"Failed to add account '{name}': {e}", exc_info=True)
        session.rollback()
        raise

def delete_account(session: Session, account_id: int):
    """
    Deletes an account by ID.

    Parameters:
        session (Session): Active database session.
        account_id (int): The ID of the account to delete.

    Returns:
        bool: True if the account was deleted, False if not found.
    """
    try:
        account = session.query(models.Account).filter_by(id=account_id).first()
        if not account:
            logger.debug(f"Attempted to delete non-existent account (ID: {account_id})")
            return False

        session.delete(account)
        session.commit()

        logger.debug(f"Account deleted (ID: {account_id})")

        return True
    except SQLAlchemyError as e:
        logger.error(f"Failed to delete account (ID: {account_id}): {e}", exc_info=True)
        session.rollback()
        raise

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
    try:
        balance_entry = models.AccountBalance(account_id=account_id, date=date, balance=balance)
        session.add(balance_entry)
        session.commit()

        logger.debug(f"Balance updated for Account ID {account_id} on {date}: {balance}")

        return balance_entry
    except SQLAlchemyError as e:
        logger.error(f"Failed to update balance for Account ID {account_id} on {date}: {e}", exc_info=True)
        session.rollback()
        raise

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
    try:
        new_transaction = models.Transaction(
            account_id=account_id,
            date=date,
            amount=amount,
            category=category,
            description=description
        )
        session.add(new_transaction)
        session.commit()

        logger.debug(f"Transaction added: Account ID {account_id}, Date: {date}, Amount: {amount}, Category: {category}")

        return new_transaction
    except SQLAlchemyError as e:
        logger.error(f"Failed to add transaction for Account ID {account_id} on {date}: {e}", exc_info=True)
        session.rollback()
        raise
