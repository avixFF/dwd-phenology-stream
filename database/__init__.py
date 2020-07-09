import os
from peewee import MySQLDatabase
from playhouse.migrate import MySQLMigrator

connection = MySQLDatabase(
    database=os.getenv('MYSQL_DATABASE'),
    host=os.getenv('MYSQL_HOST', '127.0.0.1'),
    port=int(os.getenv('MYSQL_PORT', 3306)),
    user=os.getenv('MYSQL_USERNAME'),
    password=os.getenv('MYSQL_PASSWORD'),
)

migrator = MySQLMigrator(connection)
