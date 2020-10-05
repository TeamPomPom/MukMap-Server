import sys
import logging
import mysql.connector
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

rds_host = os.environ.get("DB_HOST")
db_name =  os.environ.get("DB_NAME")
user_name =  os.environ.get("DB_USER")
password =  os.environ.get("DB_PASSWORD")
port = os.environ.get("DB_PORT")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Command(BaseCommand):
    help = 'Creates the initial database'

    def handle(self, *args, **options):
        print('Starting db creation')
        try:
            db = mysql.connector.connect(host=rds_host, user=user_name,
                                 password=password, db="mysql", connect_timeout=5)
            c = db.cursor()
            print("connected to db server")
            c.execute("""CREATE DATABASE meok_test_db;""")
            c.execute("""GRANT ALL ON meok_test_db.* TO 'meok_admin'@'%'""")
            c.close()
            print("closed db connection")
        except mysql.connector.Error as err:
            logger.error("Something went wrong: {}".format(err))
            sys.exit()
            