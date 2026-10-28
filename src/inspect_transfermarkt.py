#import duckdb so we can query the db file
import duckdb

#import Path t construct the db file path
from pathlib import Path

database_path = Path(
    "data/raw/transfermarkt/transfermarkt-datasets.duckdb"
)

connections = duckdb.connect(
    str(database_path), read_only=True,
)

try:
    #retrieve all the table names in the db
    tables = connections.execute("SHOW TABLES").fetchdf()

    #print the available tables
    print("\nDATABASE TABLES")
    print(tables.to_string(index=False))

    #inspect the columns and data types in each table
    for table_name in tables['name']:
        #table names come from db itself. double quotes allow SQL to handle names safely
        quoted_table = '"' + table_name.replace('"','""') + '"'
        #read the table schema w/o loading its full contents.
        schema = connections.execute(
            f"DESCRIBE SELECT * FROM {quoted_table}"
        ).fetchdf()

        #display each table's col names and data types
        print(f"\nSCHEMA: {table_name}")
        print(schema[["column_name","column_type"]].to_string(index=False))
finally:
    connections.close()