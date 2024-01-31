import pandas as pd
import sqlite3


class ExcelToSQLite():

    def __init__(self, excel_file_path, sqlite_db_path):
        self.excel_file_path = excel_file_path
        self.sqlite_db_path = sqlite_db_path

    def process_excel_and_insert_into_db(self):
        casse_caroline_types = ["Périmés_Rebut", "Produits_cassés", "Vol",
                                "Marchandise_donnée", "Alertnet", "Sinistre_assuré"]
        # Iteriere über die Blätter 1 bis 6
        for sheet_number in range(1, 7):
            sheet_name = f'Sheet{sheet_number}'
            df = pd.read_excel(self.excel_file_path, sheet_name, header=6)
            df = df.loc[:, ~df.columns.str.contains(
                "Unnamed: 0|Unnamed: 1|Unnamed: 4|Unnamed: 6")]
            df.rename(columns={'Unnamed: 2': "Index"}, inplace=True)

            # Extrahiere den Wert aus der Zelle C5
            week_value = pd.read_excel(self.excel_file_path, sheet_name, header=None, usecols=[2], nrows=1).iloc[0, 0]
            
            # Füge die neue Spalte 'week' mit dem extrahierten Wert hinzu
            df['week'] = week_value

            connection = sqlite3.connect(self.sqlite_db_path)
            df.to_sql(name=f"casse_caroline_{casse_caroline_types[sheet_number-1]}", con=connection,
                      if_exists="append", index=False)

            connection.commit()
            connection.close()


df = pd.read_excel("./data/CASSE CAROLINE.xlsx", header=6)
df = df.loc[:, ~df.columns.str.contains(
    "Unnamed: 0|Unnamed: 1|Unnamed: 4|Unnamed: 6")]
df.rename(columns={'Unnamed: 2': "Index"}, inplace=True)

connection = sqlite3.connect("database.db")
df.to_sql(name="casse_caroline", con=connection,
          if_exists="append", index=False)

connection.commit()
connection.close()
