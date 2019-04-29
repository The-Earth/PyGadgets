# sqltool

Incomplete upper level api connects SQLite database, based on sqlite3. Try to be much more lazier!

## Class Database

Create connection with database file. 

**table(self, name, \*\*col)** Create Table object using the same `sqlite3.Connection`. `name` is obviously the name of data table. `**col` accept keyword arguments which is required if the table does not exist. 

Examples:

```python
import sqltool

db = sqltool.Database('db.db')
# Create a table with some keys and types given.
table_1 = db.table('Table1', Name='VARCHAR(32)', ID='INT')
```

Keyword arguments will only have effects when there's no table named `name`, otherwise they will be ignored. If we want to set a primary key, add "PRIMARY KEY" in their "types". Example: `db.table('Table1', Name='VARCHAR(32)', ID='INT PRIMARY KEY')`

**get_tables(self)** returns a tuple containing information about tables in the database.

## Class Table

Read and write tables.

In common cases, we should create a Table object through `table()` method in Class Database. If we are in special cases, call initialize method: `__init__(self, conn: sqlite3.Connection, name, **col)`. Connection to SQLite database will be set manually.

**get_structure(self)** returns raw structure information in a list.

**get_columns(self)** returns name of columns and their data typles in a tuple.

**get_all(self)** returns all data in a list.

**insert(self, \*\*datadict)** inserts data given in keyword parameters to the table. Example:

```python
import sqltool

db = sqltool.Database('db.db')
table_1 = db.table('Table1', Name='VARCHAR(32)', ID='INT')
table_1.insert(Name='Alice', ID=1)
```

sqltool will configure data type by itself so there's no need to use `ID='1'`.

**update(self, datadict: dict, \*\*where)** updates existing record. `datadict` accepts new data to be written. `**where` records filter conditions of records to be updated (Used in "Where" sentence in SQLite) Example:

```python
import sqltool

db = sqltool.Database('db.db')
table_1 = db.table('Table1', Name='VARCHAR(32)', ID='INT')
table_1.insert(Name='Alice', ID=1)
table_1.update({'Name':'Bob', 'ID':2}, ID=1)
```

This will update records which have ID=1 to Name=Bob and ID=2.

**delete(self, \*\*where)** deletes records meets conditions defined in `**where`.

```python
import sqltool

db = sqltool.Database('db.db')
table_1 = db.table('Table1', Name='VARCHAR(32)', ID='INT')
table_1.insert(Name='Alice', ID=1)
table_1.delete(ID=1)
```

**lookup(self, \*\*where)** find records and return in a list. Similar usage of keyword arguments as previous mentioned methods.

**import_csv(self, filename)** imports data from CSV file to the table. It runs `insert()` method so that it could throw same exceptions as `insert()`. Example; We have a table defined as below

```python
import sqltool

db = sqltool.Database('db.db')
table_1 = db.table('Table1', Name='VARCHAR(32)', ID='INT')
```

and the CSV file should be in this format:

```csv
Name, ID
Alice, 1
Bob, 2
Charlie, 3
```

then, `table_1.import _csv('data.csv')`.

**export_csv(self, filename)** exports all data in the table to given filename in csv format.
