from dotenv import load_dotenv
import os

class SQL_CREDENTIALS:
    DBUSER = os.getenv('DBUSER')
    DBPASS = os.getenv('DBPASS')
    DBHOST = os.getenv('DBHOST')
    DBNAME = os.getenv('DBNAME')

SQL_CFG = {
    'user': SQL_CREDENTIALS.DBUSER,
    'password': SQL_CREDENTIALS.DBPASS,
    'dbhostname': SQL_CREDENTIALS.DBHOST,
    'dbname': SQL_CREDENTIALS.DBNAME
}