from db_operations import db_operations


def create_rider_table(db_ops):
    query = """
    CREATE TABLE Rider (
        rider_id    INT AUTO_INCREMENT PRIMARY KEY,
        username    VARCHAR(50) NOT NULL UNIQUE,
        first_name  VARCHAR(50) NOT NULL,
        last_name   VARCHAR(50) NOT NULL
    );
    """
    db_ops.modify_query(query)
    print("Rider table created")


def create_driver_table(db_ops):
    query = """
    CREATE TABLE Driver (
        driver_id   INT AUTO_INCREMENT PRIMARY KEY,
        username    VARCHAR(50) NOT NULL UNIQUE,
        first_name  VARCHAR(50) NOT NULL,
        last_name   VARCHAR(50) NOT NULL,
        driver_mode BOOLEAN NOT NULL DEFAULT FALSE
    );
    """
    db_ops.modify_query(query)
    print("Driver table created")


# Both FKs live on Ride: it's the N side of Rider-Takes-Ride and
# Driver-Gives-Ride. Driver's average rating is derived with
# AVG(rating), not stored (keeps 3NF).
def create_ride_table(db_ops):
    query = """
    CREATE TABLE Ride (
        ride_id          INT AUTO_INCREMENT PRIMARY KEY,
        rider_id         INT NOT NULL,
        driver_id        INT NOT NULL,
        pickup_location  VARCHAR(100) NOT NULL,
        dropoff_location VARCHAR(100) NOT NULL,
        ride_datetime    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        rating           TINYINT NULL,
        CHECK (rating BETWEEN 1 AND 5),
        FOREIGN KEY (rider_id)  REFERENCES Rider(rider_id),
        FOREIGN KEY (driver_id) REFERENCES Driver(driver_id)
    );
    """
    db_ops.modify_query(query)
    print("Ride table created")

# creates missing tables
def create_tables(db_ops):
    if not db_ops.does_table_exist("Rider"):
        create_rider_table(db_ops)
    if not db_ops.does_table_exist("Driver"):
        create_driver_table(db_ops)
    if not db_ops.does_table_exist("Ride"):
        create_ride_table(db_ops)


# delete / drop all tables
def reset_tables(db_ops):
    db_ops.modify_query("DROP TABLE IF EXISTS Ride;")
    db_ops.modify_query("DROP TABLE IF EXISTS Rider;")
    db_ops.modify_query("DROP TABLE IF EXISTS Driver;")
    create_tables(db_ops)
