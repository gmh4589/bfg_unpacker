import sqlalchemy
import pandas


class DatabaseConnect:
    _instance = None

    def __init__(self, db_path="sqlite:///game_base.db"):
        self.engine = sqlalchemy.create_engine(db_path)
        self.conn = self.engine.connect()
        self.metadata = sqlalchemy.MetaData()

    def __new__(cls, *args, **kwargs):

        if cls._instance is None:
            cls._instance = super(DatabaseConnect, cls).__new__(cls)

        return cls._instance
    
    def get_table(self, table_name, filter=False, column_name='skip', value=0):
        db_table = sqlalchemy.Table(table_name, self.metadata, autoload_with=self.engine)

        if filter:
            query = sqlalchemy.select(db_table).where(db_table.c[column_name] == value)
        else:
            query = sqlalchemy.select(db_table)

        return pandas.read_sql_query(query, self.conn)
    
    def disconnect(self):
        self.conn.close()
