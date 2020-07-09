import os
from peewee import MySQLDatabase
from playhouse.migrate import MySQLMigrator

connection = MySQLDatabase(
    database=os.getenv('MYSQL_DATABASE')
)

migrator = MySQLMigrator(connection)
