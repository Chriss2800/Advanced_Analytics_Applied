import pandas as pd
import sqlite3
import tabula
from datetime import datetime
import re


class FileToSQLite():

    def __init__(self) -> None:
        self.sqlite_db_path = "database.db"

    def process_anacamarge_synthese_xlsx(self, excel_file, selected_week):
        try:
            df = pd.read_excel(excel_file, header=[2, 3])
            df.rename(
                columns={
                    'Unnamed: 5': df.columns[4],
                    'Unnamed: 6': df.columns[4],
                    'Unnamed: 8': df.columns[7],
                    'Unnamed: 9': df.columns[7],
                    'Unnamed: 11': df.columns[10],
                    'Unnamed: 12': df.columns[10],
                }, inplace=True)
            column_names = [
                ' '.join(filter(pd.notna, col)) for col in df.columns]
            df.columns = [col.replace('.', '') for col in column_names]
            df.columns = df.columns.astype(str).str.replace('\n', ' ')

            df = df.drop([df.columns[0], df.columns[3]], axis=1)
            df.rename(
                columns={
                    'Unnamed: 1_level_0 Unnamed: 1_level_1': 'Id',
                    'Unnamed: 2_level_0 Unnamed: 2_level_1': 'Category'
                }, inplace=True)
            df = df.iloc[:-2]
            df['upload_date'] = pd.to_datetime(
                datetime.today().strftime('%d-%m-%Y'))
            df['report week'] = selected_week
            connection = sqlite3.connect(self.sqlite_db_path)
            df.to_sql(name="anacamarge_synthese", con=connection,
                      if_exists="append", index=False)

            connection.commit()
            connection.close()

        except Exception as e:
            print(f"Error: {e}")

    def process_ca_bench_reporting_factorie_pdf(self, pdf_file, selected_week):
        try:
            df = tabula.read_pdf(pdf_file, pages='all',
                                 multiple_tables=False)[0]
            journee_value = df.iloc[0, 3].split(" ")[0]
            df = df.drop([0, 1, 2])
            df = df.drop(df.columns[-1], axis=1)
            df = df[df.iloc[:, 0] != "SURFACE DE VENTE"]
            df = df.dropna(subset=[df.columns[0]])
            df = df.reset_index(drop=True)
            column_names = [
                'SURFACE DE VENTE',
                f"{journee_value} CA TTC K€",
                f"{journee_value} CA TTC % Evol",
                f"{journee_value} Débits Nbre",
                f"{journee_value} Débits % Evol",
                f"{journee_value} Panier €",
                f"{journee_value} Panier % Evol",
                "Semaine à date CA TTC K€",
                "Semaine à date CA TTC % Evol",
                "Semaine à date Débits Nbre",
                "Semaine à date Débits % Evol",
                "Semaine à date Panier €",
                "Semaine à date Panier % Evol",
                "Actualisé Mois CA TTC K€",
                "Actualisé Mois CA TTC % Evol",
            ]
            df.columns = column_names
            df['upload_date'] = pd.to_datetime(
                datetime.today().strftime('%d-%m-%Y'))
            df['report week'] = selected_week
            connection = sqlite3.connect(self.sqlite_db_path)
            df.to_sql(name="ca_bench_reporting_factorie", con=connection,
                      if_exists="append", index=False)

            connection.commit()
            connection.close()

        except Exception as e:
            print(f"Error: {e}")

    def process_ca_ht_caroline_pdf(self, pdf_file, selected_week):
        try:
            df = tabula.read_pdf(pdf_file,
                                 pages='all', multiple_tables=False)[0]
            df['Rayon'].fillna(method='ffill', inplace=True)
            df = df[df.iloc[:, 0] != "Rayon"]
            df.reset_index(drop=True)
            df['upload_date'] = pd.to_datetime(
                datetime.today().strftime('%d-%m-%Y'))
            df['report week'] = selected_week
            connection = sqlite3.connect(self.sqlite_db_path)
            df.to_sql(name="ca_ht_caroline", con=connection,
                      if_exists="append", index=False)

            connection.commit()
            connection.close()

        except Exception as e:
            print(f"Error: {e}")

    def process_ca_market_caroline_super_pdf(self, pdf_file, selected_week):
        try:
            df = tabula.read_pdf(pdf_file, pages='all',
                                 multiple_tables=False)[0]
            df['upload_date'] = pd.to_datetime(
                datetime.today().strftime('%d-%m-%Y'))
            df['report week'] = selected_week
            connection = sqlite3.connect(self.sqlite_db_path)
            df.to_sql(name="ca_market_caroline_super", con=connection,
                      if_exists="append", index=False)

            connection.commit()
            connection.close()

        except Exception as e:
            print(f"Error: {e}")

    def process_casse_caroline_xlsx(self, excel_file, selected_week):
        try:
            dfs = []
            sheet_names = pd.ExcelFile(excel_file).sheet_names

            for sheet_number in range(len(sheet_names)):
                sheet_name = f'Sheet{sheet_number+1}'
                df = pd.read_excel(excel_file, sheet_name, header=6)
                df = df.loc[:, ~df.columns.str.contains(
                    "Unnamed: 0|Unnamed: 1|Unnamed: 4|Unnamed: 6")]
                df.columns = [re.sub(r'\s+', ' ', col) for col in df.columns]
                df.rename(columns={'Unnamed: 2': "Index"}, inplace=True)

                df['sheet_name'] = sheet_name
                df['upload_date'] = pd.to_datetime(
                    datetime.today().strftime('%d-%m-%Y'), dayfirst=True)
                df['report week'] = selected_week
                dfs.append(df)

            result_df = pd.concat(dfs, ignore_index=True)

            connection = sqlite3.connect(self.sqlite_db_path)
            result_df.to_sql(name="casse_caroline", con=connection,
                             if_exists="append", index=False)

            connection.commit()
            connection.close()

        except Exception as e:
            print(f"Error: {e}")
