from pathlib import Path #to work with files and folders
import pandas as pd #to read and manipulate the csv datasets

DATA_DIR = Path("data/raw") #directory containign our downlaoded datasets
#find every csv files inside data/raw including its subfolders
for file in sorted(DATA_DIR.rglob("*.csv")):
    print("\n" + "=" * 80)
    print(f"FILE: {file}")

    try:
        #load the csvs into a pandas dataframe
        df = pd.read_csv(file, low_memory = False)

        #display the dataset'd dimension to display its size
        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")

        #display column names to identify useful features and target variables
        print("\nColumn names: ")
        print(df.columns.tolist())

        #display 3 sample rows to understand the data's structure
        print("\nFirst 3 rows: ")
        print(df.head(3).to_string(index=False))

        #count missing values to identify potential data-cleaning requirements
        print("\nMissing Values: ")
        print(
            df.isnull()
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

    except Exception as e:
        #report errors for individual files w/o stopping the entire inspection
        print(f"Could not read file: {e}")

