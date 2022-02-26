import mysql.connector
from flask import request

class Database:
    #constructor
    def __init__(self):
        self.initiate_connection()

    def initiate_connection(self):
        try:
            # making connection with our sql (mysql)server
            cnx = mysql.connector.connect(
                host="127.0.0.1",
                database="stocks",
                port=3306,
                user="root",
                password="12345678")
             
            self.cnx = cnx
        except:
            self.cnx = None

    def delete_holding(self, symbol):
        if self.cnx == None:
            raise Exception("Database connection failed")
        #cursor is used to execute statements to communicate with the MySQL database
        cur = self.cnx.cursor()

        data = (                #prevents sql injection
            symbol,
        );

        query = "DELETE FROM holdings WHERE symbol = %s"
        #executing the query
        cur.execute(query, data)
        #if a function doesn't return something we have to commit it.
        self.cnx.commit()
        #closing the cursor
        cur.close()

    def add_holding(self,symbol,quantity,price,date,notes,uname):
        if self.cnx == None:
            raise Exception("Database connection failed")

        cur = self.cnx.cursor()

        #variable to which we have assigned our sql query
        add_holding = ("INSERT INTO holdings "
               "(symbol, quantity, price, date, notes, U_Name) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        #variable in which our sql query data is saved
        data_holding=(symbol, quantity, price, date, notes, uname,)
        #executing our both variables
        
        cur.execute(add_holding, data_holding)
        

        # Make sure data is committed to the database
        self.cnx.commit()
        cur.close()

    def get_holdings(self, uname):
        if self.cnx == None:
            raise Exception("Database connection failed")

        cur = self.cnx.cursor()
        data=(uname,)
        query = "SELECT * FROM holdings WHERE U_Name=%s"
        print("HERE get holdingsss")
        cur.execute(query,data)
        
        holdings = []
        print(cur)
        for (symbol, quantity, price, date, notes,uname) in cur:
            holdings.append(
                (
                    symbol,
                    quantity,
                    price,
                    date,
                    notes,
                    uname,
                )
            )
        cur.close()
        return holdings

    def get_user(self, name, email):
        print("enetered get_user")
        if (self.cnx==None):
            raise Exception("Database connection failed")
        cur = self.cnx.cursor()
        data=(
            name,
            email,
        )

        q="SELECT * FROM user where name=%s or email=%s"
        cur.execute(q,data)
        print(q)
        user=[]
        for (name,email, password) in cur:
            user.append((name,email,password))
        self.cnx.commit()
        cur.close()    
        return user

    def fetch_user(self,name,password):
        if (self.cnx==None):
            raise Exception("Database connection failed")
        cur = self.cnx.cursor()
        user=[]
        query=("SELECT * FROM user WHERE name=%s AND password=%s")
        data=(name,password)
        cur.execute(query,data)
        for(name,email,password) in cur:
            user.append((name,email,password))
        self.cnx.commit()
        cur.close()    
        return user

    def register(self,name,email,password):
        if (self.cnx==None):
            raise Exception("Database connection failed")
        cur = self.cnx.cursor()
        print("register")
        st=("INSERT INTO user values(%s,%s,%s)")
        user=(name,email,password)
        cur.execute(st,user)
        print("after getuser")
        self.cnx.commit()
        cur.close()

    def get_holding(self, symbol, uname):
        if self.cnx == None:
            raise Exception("Database connection failed")

        cur = self.cnx.cursor()

        data = (                #prevents sql injection
            symbol,
            uname,
        )

        fetch_holding=("SELECT * "
                " FROM holdings "
                " WHERE symbol=%s "
                "AND U_Name=%s")
        cur.execute(fetch_holding,data)
        #list that have tuples (holdings of our database) as their elements.
        holdings = []

        for (symbol, quantity, price, date, notes,uname) in cur:
            #appending means adding (adding our tuple in the list(holdings[]))
            holdings.append(
                (
                    symbol,
                    quantity,
                    price,
                    date,
                    notes,
                    uname,
                )
            )
        cur.close()
        return holdings

    def update_holding(self, symbol, quantity, price, date, notes):
        if self.cnx == None:
            raise Exception("Database connection failed")

        cur = self.cnx.cursor()
        data = (                #prevents sql injection
            quantity,
            price,
            date,
            notes,
            symbol,
        );

        update_holding = ("UPDATE holdings "
               " SET quantity = %s, price = %s, date = %s, notes = %s "
               " WHERE symbol = %s ")

        cur.execute(update_holding, data)

        # Make sure data is committed to the database
        self.cnx.commit()
        #closing cursor
        cur.close()
    # destructor- called when all references to the object have been deleted i.e when an object is garbage collected(also deleted when the object goes out of reference or when the program ends).
    def __del__(self):
        if self.cnx == None:
            raise Exception("Database connection failed")
            #closing the connection
        self.cnx.close()