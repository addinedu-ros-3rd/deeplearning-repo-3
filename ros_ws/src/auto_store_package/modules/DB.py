import mysql.connector
import configparser
import Logger

config = configparser.ConfigParser()
config.read('config.ini')
dev = config['dev']

log = Logger()

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
   
        except Exception as e:
            log.error(f" DB __init__ : {e}")
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

        except Exception as e:
            log.error(f" DB execute : {e}")

        finally:
            self.disconnect()


    def fetchOne(self):
        try:
            self.checkIfConnected()
            return self.cursor.fetchone()[0]

        except Exception as e:
            log.error(f" DB fetchOne : {e}")

        finally:
            self.disconnect()


    def fetchAll(self):
        try:
            self.checkIfConnected()
            return self.cursor.fetchall()

        except Exception as e:
            log.error(f" DB fetchAll : {e}")

        finally:
            self.disconnect()