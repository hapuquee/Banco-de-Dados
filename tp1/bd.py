import psycopg2

# Connect to your postgres DB
con = psycopg2.connect(host='172.17.0.2',  
                       user='postgres', 
                       password='1234')

con.autocommit = True

# Open a cursor to perform database operations
cur = con.cursor()

# Execute a query
cur.execute("CREATE DATABASE TP1BD")

# Retrieve query results
records = cur.fetchall()

cur.close()
con.close()

print(f"records: {records}")