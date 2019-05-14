import sqlite3
import csv


class Database:
    def __init__(self, filename):
        self.filename = filename
        self.__conn = sqlite3.connect(filename)

    def table(self, name, **col):
        return Table(self.__conn, name, **col)

    def get_tables(self) -> tuple:
        cur = self.__conn.execute("select name from sqlite_master where type='table' order by name")
        return cur.fetchall()[0]

    def __del__(self):
        self.__conn.commit()
        self.__conn.close()


class Table:
    def __init__(self, conn: sqlite3.Connection, name, **col):
        self.__conn = conn
        self.__cur = self.__conn.cursor()
        self.name = name
        # Create table if not exists
        if not self.__exists():
            if len(col) == 0:
                raise TableNotFoundError(f"Table {name} not found. Keys and types needed to initialize one.")
            cmd = f"CREATE TABLE {name}("
            for item in col:
                cmd += f"{item} {col[item]}, "
            cmd = cmd.strip(", ") + ");"
            self.__cur.execute(cmd)
            self.__conn.commit()

    def __exists(self) -> bool:
        self.__cur.execute(f"select count(*) from sqlite_master where type='table' and name = '{self.name}'")
        return bool(int(self.__cur.fetchall()[0][0]))

    @staticmethod
    def __data_pretreat(data):    # Transform to SQL format (str and numbers only)
        if isinstance(data, str):
            return f"\'{data}\'"
        elif isinstance(data, int) or isinstance(data, float):
            return str(data)
        else:
            return data

    def get_structure(self) -> list:
        self.__cur.execute(f"PRAGMA table_info({self.name})")
        return self.__cur.fetchall()

    def get_columns(self) -> tuple:
        structure = self.get_structure()
        column = ()
        for i in range(len(structure)):
            column += tuple(structure[i][1:2])
        return column

    def get_all(self) -> list:
        self.__cur.execute(f"Select * from {self.name}")
        return self.__cur.fetchall()

    def insert(self, **datadict):
        for key in datadict:
            datadict[key] = self.__data_pretreat(datadict[key])

        command = "INSERT into %s (%s) values (%s)" % (
            self.name, ', '.join(datadict.keys()), ','.join(datadict.values()))

        try:
            self.__cur.execute(command)
            self.__conn.commit()
        except sqlite3.IntegrityError as e:
            conflict_key = e.args[0].split('.')[-1]
            raise KeyConflictError(f"Value of key '{conflict_key}' conflicts with existing item")
        except sqlite3.OperationalError as e:
            if e.args[0].startswith(f"table {self.name} has no column named"):
                problem_name = e.args[0].split()[-1]
                raise KeyNotFoundError(f"Key '{problem_name}' not found.")
            else:
                raise

    def update(self, datadict: dict, **where):
        where_key = list(where.keys())[0]
        where_value = list(where.values())[0]
        for key in datadict:
            datadict[key] = self.__data_pretreat(datadict[key])
        where_value = self.__data_pretreat(where_value)
        # Making up update commands
        command = f'UPDATE {self.name} set '

        for key in datadict.keys():
            command += f'{key} = {datadict[key]}, '
        command = command.strip(', ') + f' where {where_key} = {where_value}'

        try:
            self.__cur.execute(command)
            self.__conn.commit()
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such column:'):
                problem_name = e.args[0].split()[-1]
                raise KeyNotFoundError(f"Key '{problem_name}' not found.")
            else:
                raise

    def delete(self, **where):
        where_key = list(where.keys())
        where_value = list(where.values())
        for i in range(len(where_value)):
            where_value[i] = self.__data_pretreat(where_value[i])

        command = f"DELETE from {self.name} where "
        for i in range(len(where_key)):
            command += f"{where_key[i]} = {where_value} AND "
        command = command.rstrip("AND ")

        try:
            self.__cur.execute(command)
            self.__conn.commit()
        except sqlite3.OperationalError as e:
            if e.args[0].startswith('no such column:'):
                problem_name = e.args[0].split()[-1]
                raise KeyNotFoundError(f"Key '{problem_name}' not found.")
            else:
                raise

    def lookup(self, **where) -> list:
        where_key = list(where.keys())
        where_value = list(where.values())
        for i in range(len(where_value)):
            where_value[i] = self.__data_pretreat(where_value[i])

        command = f"Select * from {self.name} where "
        for i in range(len(where_key)):
            command += f"{where_key[i]} = {where_value[i]} AND "
        command = command.rstrip("AND ")

        self.__cur.execute(command)
        fetch = self.__cur.fetchall()
        if len(fetch) == 0:
            raise KeyNotFoundError(f"No record meets the condition '{where_key} = {where_value}'.")

        target = []
        for index in range(len(fetch)):
            temp_dict = {}
            for i in range(len(fetch[index])):
                temp_dict[self.get_structure()[i][1]] = fetch[index][i]
            target.append(temp_dict)
        return target

    def import_csv(self, filename):
        csv_list = list(csv.reader(open(filename, 'r')))
        for i in range(len(csv_list)):
            if i == 0:
                continue
            row_dict = dict()
            for j in range(len(csv_list[i])):
                row_dict[csv_list[0][j]] = csv_list[i][j]

            self.insert(**row_dict)

    def export_csv(self, filename):
        self.__cur.execute(f'Pragma table_info({self.name})')
        temp_key = self.__cur.fetchall()
        keys = []
        for entry in temp_key:
            keys.append(entry[1])

        self.__cur.execute(f'Select * from {self.name}')
        temp_val = self.__cur.fetchall()

        csv_writer = csv.writer(open(filename, 'a', newline=''))
        csv_writer.writerow(keys)
        for entry in temp_val:
            csv_writer.writerow(entry)


class TableNotFoundError(sqlite3.OperationalError):
    pass


class KeyConflictError(sqlite3.IntegrityError):
    pass


class KeyNotFoundError(sqlite3.OperationalError):
    pass
