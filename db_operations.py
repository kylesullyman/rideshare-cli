import mysql.connector
from helper import data_cleaner

class db_operations:
    def __init__(self, host="localhost", user="root", password="databaseP",
                 database="RideShare"):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            auth_plugin='mysql_native_password',
            database=database
        )
        self.cursor = self.connection.cursor()
        print("connection made..")

    def modify_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def modify_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()
        return self.cursor.lastrowid

    def select_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchall()

    def single_row_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchone()

    def single_record_params(self, query, dictionary):
        row = self.single_row_params(query, dictionary)
        return None if row is None else row[0]

    # ---- AI-generated (Claude), see ai_transcript_db_operations.md ----
    def bulk_insert(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()
    # ---- end AI-generated ----

    # MySQL keeps table info in information_schema instead of sqlite_master
    def does_table_exist(self, table_name):
        query = """
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = DATABASE() AND table_name = %(name)s;
        """
        return self.single_record_params(query, {"name": table_name}) == 1

    # ---- AI-generated (Claude), see ai_transcript_db_operations.md ----
    def is_table_empty(self, table_name):
        query = f"SELECT COUNT(*) FROM {table_name};"
        return self.single_record_params(query, {}) == 0

    # fill empty tables
    def populate_tables(self, rider_path, driver_path, ride_path):
        if self.is_table_empty("Rider"):
            query = """
            INSERT INTO Rider (rider_id, username, first_name, last_name)
            VALUES (%s, %s, %s, %s);
            """
            self.bulk_insert(query, data_cleaner(rider_path))
            print("Rider sample data loaded")

        if self.is_table_empty("Driver"):
            query = """
            INSERT INTO Driver (driver_id, username, first_name, last_name,
                                driver_mode)
            VALUES (%s, %s, %s, %s, %s);
            """
            self.bulk_insert(query, data_cleaner(driver_path))
            print("Driver sample data loaded")

        if self.is_table_empty("Ride"):
            query = """
            INSERT INTO Ride (ride_id, rider_id, driver_id, pickup_location,
                              dropoff_location, ride_datetime, rating)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            self.bulk_insert(query, data_cleaner(ride_path))
            print("Ride sample data loaded")
    # ---- end AI-generated ----

    def destructor(self):
        self.cursor.close()
        self.connection.close()
