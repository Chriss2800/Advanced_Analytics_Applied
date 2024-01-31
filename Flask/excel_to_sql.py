import pandas as pd
import sqlite3


class ExcelToSQLite():

    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.sqlite_db_path = "database.db"
        self.casse_caroline_types = ["Périmés_Rebut", "Produits_cassés", "Vol",
                                "Marchandise_donnée", "Alertnet", "Sinistre_assuré"]

    def process_excel_and_insert_into_db(self):
        
        # Iteriere über die Blätter 1 bis 6
        for sheet_number in range(len(self.casse_caroline_types)):
            sheet_name = f'Sheet{sheet_number+1}'
            df = pd.read_excel(self.excel_file_path, sheet_name, header=6)
            df = df.loc[:, ~df.columns.str.contains(
                "Unnamed: 0|Unnamed: 1|Unnamed: 4|Unnamed: 6")]
            df.rename(columns={'Unnamed: 2': "Index"}, inplace=True)

            # Extrahiere den Wert aus der Zelle C5
            df['week'] = pd.read_excel(self.excel_file_path, sheet_name, header=None, usecols=[2], nrows=5).iloc[-1, 0]
           

            connection = sqlite3.connect(self.sqlite_db_path)
            df.to_sql(name=f"casse_caroline_{self.casse_caroline_types[sheet_number]}", con=connection,
                      if_exists="append", index=False)

            connection.commit()
            connection.close()

ets = ExcelToSQLite(excel_file_path="./data/CASSE CAROLINE.xlsx")
ets.process_excel_and_insert_into_db()
