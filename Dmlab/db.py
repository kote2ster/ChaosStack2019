import sqlite3
from sqlite3 import Error


class DB:
    conn = None
    houses_table_name = 'houses'
    sql_create_houses_table = """ CREATE TABLE IF NOT EXISTS {0} (
                                    id integer PRIMARY KEY,
                                    place text NOT NULL,
                                    price text NOT NULL,
                                    property text NOT NULL,
                                    balcony text NOT NULL,
                                    room text NOT NULL,
                                    small_room text NOT NULL,
                                    condition text NOT NULL,
                                    floor text NOT NULL,
                                    views text NOT NULL,
                                    date text NOT NULL
                                ); """.format(houses_table_name)
    
    def __init__(self, db_file):
        self.create_connection(db_file)

    def create_table(self, create_table_sql=sql_create_houses_table):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            c.execute('DELETE FROM ' + self.houses_table_name)
            self.conn.commit()
        except Error as e:
            print(e)
    
    def insert_house(self, house):
        house_prop_list = [
            house['place'], house['price'], house['property'],
            house['balcony'], house['room'], house['small room'],
            house['condition'], house['floor'], house['views'], house['date']
        ]
        sql = ''' INSERT INTO houses(place, price, property, balcony, room, small_room, condition, floor, views, date)
                VALUES(?,?,?,?,?,?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, house_prop_list)
        self.conn.commit()
        return cur.lastrowid

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

    def close(self):
        if self.conn:
            self.conn.close()
