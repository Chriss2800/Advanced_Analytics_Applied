import pandas as pd
import sqlite3

df = pd.read_excel("./data/CASSE CAROLINE.xlsx", header=6)
df = df.loc[:, ~df.columns.str.contains(
    "Unnamed: 0|Unnamed: 1|Unnamed: 4|Unnamed: 6")]
df.rename(columns={'Unnamed: 2': "Index"}, inplace=True)

connection = sqlite3.connect("database.db")
df.to_sql(name="casse_caroline", con=connection,
          if_exists="append", index=False)

connection.commit()
connection.close()
