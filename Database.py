import mysql.connector
import configparser
config = configparser.ConfigParser()

config.read('config.ini')
dev = config['dev']

class DB():
    
    def __init__(self):
        try:
            host = dev['host']
            port = dev['port']
            user = dev['user']
            password = dev['password']
            database = dev['database']
            
            self.conn = mysql.connector.connect(host = host, 
                                                port = port, 
                                                user = user, 
                                                password = password, 
                                                database = database)
            self.cursor = self.conn.cursor(buffered=True)
            print("connect!")
        except Exception as e:
            print(f" DB __init__ : {e}")
            self.conn = None


    def disconnect(self):
        self.cursor.close()
        self.conn.close()
            
            
    def checkIfConnected(self):
        if not self.conn:
            raise Exception("Not connected to the database. Call connect() method first.")
            

    def execute(self, query, params=None):
        try:
            self.checkIfConnected()
            self.cursor.execute(query, params)
            self.conn.commit()
            print("execute")

        except Exception as e:
            print(f" DB execute : {e}")

        finally:
            self.disconnect()


    def fetchOne(self):
        try:
            self.checkIfConnected()
            print("fetchOne")
            return self.cursor.fetchone()[0]

        except Exception as e:
            print(f" DB fetchOne : {e}")

        finally:
            self.disconnect()


    def fetchAll(self):
        try:
            self.checkIfConnected()
            print("fetchAll")
            return self.cursor.fetchall()

        except Exception as e:
            print(f" DB fetchAll : {e}")

        finally:
            self.disconnect()