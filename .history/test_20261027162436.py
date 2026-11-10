import mysql.connector 
mydb = mysql.connector.connect(host="localhost",
    user="root",
    password="cR(=bl1H8Nhd",
    auth_plugin='mysql_native_password')
print(mydb)
mydb.close()