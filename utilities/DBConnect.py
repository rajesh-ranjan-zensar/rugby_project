import mysql.connector
from mysql.connector import Error


class MySqlDB:
    LogUser = ""
    LogPwd = ""
    LogHostName = ""
    LogDBName = ""
    HomeContext = dict()


    def __init__(self):
        self.LogUser = ""
        self.LogPwd = ""
        self.LogHostName = ""
        self.LogDBName = ""
    def initialize(self,user, pwd, hostname, dbname):
        self.LogUser = user
        self.LogPwd = pwd
        self.LogHostName = hostname
        self.LogDBName = dbname
        print(self.LogUser + "/" + self.LogPwd + "@" + self.LogDBName)

    def connect(self):
        err_msg = ""
        try:
            self.DBcon = mysql.connector.connect(host=self.LogHostName,
                                         database=self.LogDBName,
                                         user=self.LogUser,
                                         password=self.LogPwd)
            if self.DBcon.is_connected():
                db_Info = self.DBcon.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.cursor = self.DBcon.cursor()
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)
            err_msg = 'Database connection error'

        print("Error Message: "+err_msg)
        return err_msg


