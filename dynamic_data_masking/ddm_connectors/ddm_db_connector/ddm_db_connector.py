import pyodbc
from dynamic_data_masking.ddm_logger import DynamicDataMaskingLogger
import threading

logger = DynamicDataMaskingLogger().get_logger()

class DDMDBConnect:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, server: str, db: str):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DDMDBConnect, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, server: str, db: str):
        if self._initialized:
            return
        self.server = server
        self.db = db
        self.connection = None
        self.connect_to_server()
        self._initialized = True

    def connect_to_server(self) -> pyodbc.Connection:
        if self.connection is not None:
            return self.connection

        connection_string = (
            f"DRIVER={{SQL Server}};"
            f"SERVER={self.server};"
            f"DATABASE={self.db};"
            f"Trusted_Connection=yes;"
        )
        try:
            self.connection = pyodbc.connect(connection_string)
            logger.info(f"DATABASE : CONNECTION ESTABLISHED TO {self.server}; DATABASE : {self.db}")
        except Exception as e:
            logger.error(f"DATABASE : CONNECTION TO {self.server} FAILED | ERROR: {e}")
        return self.connection

class DDMDatabaseReader:
   
    def __init__(self, server, db):
        self.db_connect = DDMDBConnect(server, db)
        self.connection = self.db_connect.connection

    @staticmethod
    def select_deny_list_query(language, category, values_table, col_name):
        return f'''
            SELECT
                deny_list.{col_name}
            FROM
                {values_table} deny_list
            JOIN
                ddm_categories categories ON categories.id = deny_list.token_category_fk
            WHERE
                language_code = '{language}'
            AND
                categories.category_name = '{category}'
        '''

    @staticmethod
    def select_params(param):
        return f'''
            SELECT
                value
            FROM
                ddm_parameters
            WHERE
                name = '{param}'
        '''

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
