import mysql.connector
from helper import get_choice, get_text
from db_operations import db_operations
from create_tables import create_tables

db_ops = db_operations()


def startScreen():
    create_tables(db_ops)
    db_ops.populate_tables("riders.csv", "drivers.csv", "rides.csv")


def start_options():
    print("""
Welcome to RideShare! Select from the following options:
    1. I don't have an account (create one)
    2. Log in as an existing rider
    3. Log in as an existing driver
    4. Exit""")
    return get_choice([1, 2, 3, 4])


def create_account():
    print("""
What kind of account would you like to create?
    1. Rider
    2. Driver""")
    account_type = "rider" if get_choice([1, 2]) == 1 else "driver"

    first_name = get_text("First name: ")
    last_name = get_text("Last name: ")

    # table name can't be a placeholder, so choose between two fixed queries
    if account_type == "rider":
        query = """
        INSERT INTO Rider (username, first_name, last_name)
        VALUES (%(username)s, %(first_name)s, %(last_name)s);
        """
    else:
        query = """
        INSERT INTO Driver (username, first_name, last_name)
        VALUES (%(username)s, %(first_name)s, %(last_name)s);
        """

    # ask for username and check unique
    while True:
        username = get_text("Choose a username: ")
        try:
            new_id = db_ops.modify_query_params(query, {
                "username": username,
                "first_name": first_name,
                "last_name": last_name
            })
            break
        except mysql.connector.IntegrityError:
            print("That username is already taken. Try another.")

    print(f"\nAccount created! Your {account_type} ID is {new_id}.")
    return account_type, new_id
