from .Database import Database


def db_execute(cmd, *args):
    '''
    Executes a line of SQL
    NOTE: Only for reading (SELECT) as it does not commit
    '''
    with Database.get_db().cursor() as cursor:
        cursor.execute(cmd, *args)
        res = cursor.fetchall()
    return res


def get_table_names():
    ''' Get table names in the connected database '''
    with Database.get_db().cursor() as cursor:
        cursor.execute('''SELECT table_name FROM information_schema.tables
        WHERE table_schema = %s;''', Database.db_name)
        table_names = cursor.fetchall()
    return [v[0] for v in table_names]


def get_table_columns(table_name):
    ''' Get the column names of a table '''
    with Database.get_db().cursor() as cursor:
        cursor.execute('''SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_name = %s;''', table_name)
        col_names = cursor.fetchall()
    return [v[0] for v in col_names]

