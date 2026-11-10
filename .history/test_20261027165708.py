#import MySQL
import mysql.connector
#Make Connection
conn = mysql.connector.connect(host="localhost",
    user="root",
    password="databaseP",
    auth_plugin='mysql_native_password',
    database='RideShare'
)
#create cursor object
cur_obj = conn.cursor()
#create database schema
#confirm execution worked by printing result
cur_obj.execute("SHOW DATABASES;")
for row in cur_obj:
    print(row)

print(conn)
conn.close