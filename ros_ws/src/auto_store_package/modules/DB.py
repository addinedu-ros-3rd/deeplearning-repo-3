import mysql.connector
import configparser
from modules.Logger import Logger
import os.path
import time


class DB():
    
    def __init__(self):
        try:
            self.config = configparser.ConfigParser()
            self.config.read('install/auto_store_package/lib/auto_store_package/modules/config.ini', encoding='utf-8')
            dev = self.config['dev']

            logfile_name = time.strftime("%Y%m%d-%H%M%S") + '.log'
            with open(logfile_name,"w") as f:
                f.close()

            self.log = Logger(logfile_name)

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
            print(f" DB __init__ : {type(e)} - {e}")
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
            self.log.error(f" DB execute : {e}")

        # finally:
        #     self.disconnect()


    def fetchone(self):
        try:
            self.checkIfConnected()
            return self.cursor.fetchone()[0]

        except Exception as e:
            self.log.error(f" DB fetchOne : {e}")

        # finally:
        #     self.disconnect()


    def fetchAll(self):
        try:
            self.checkIfConnected()
            return self.cursor.fetchall()

        except Exception as e:
            self.log.error(f" DB fetchAll : {e}")

        # finally:
        #     self.disconnect()