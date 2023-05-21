import pandas as pd
import uuid
import numpy as np

class IPSDataManager:

    def __init__(self):
        self.df_general = pd.DataFrame(columns=['FILENAME', 'PATIENT_NAME', 'PATIENT_ID', 'DATE_TEST', 'RAPPORT_ID',
                                                'DATE_NAISSANCE', 'AGE', 'SEXE'])
        self.df_detailed = pd.DataFrame(columns=['PATIENT_ID', 'DATE_TEST', 'IPS_D', 'IPS_G', 'BPM', 'BRAS_SYS', 'BRAS_DIA',
                                                 'BORNE_INF', 'BORNE_SUP'])

    def format_general_table(self, df):
        df = df.assign(
            DATE_NAISSANCE=pd.to_datetime(df['DATE_NAISSANCE'].str.strip(), format='%d/%m/%Y', errors='coerce'),
            DATE_TEST=pd.to_datetime(df['DATE_TEST'], dayfirst=True, errors='coerce')
        )
        df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')
        df[['PATIENT_NAME', 'SEXE']] = df[['PATIENT_NAME', 'SEXE']].apply(lambda x: x.str.upper())
        return df

    def format_detailed_table(self, df):
        df[['IPS_D', 'IPS_G']] = df[['IPS_D', 'IPS_G']].apply(lambda x: x.str.replace(',', '.'))
        df = df.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.name not in ['PATIENT_ID', 'DATE_TEST'] else x)
        df['DATE_TEST'] = pd.to_datetime(df['DATE_TEST'], dayfirst=True, errors='coerce')
        return df


class EFRDataManager:

    def __init__(self):
        self.df_general = pd.DataFrame(columns=[
            'FILENAME', 'PATIENT_NAME', 'PATIENT_ID', 'DATE_TEST', 'ETHNIE', 'TAILLE', 'AGE', 'SEXE', 'BMI',
            'POIDS']
        )
        self.df_detailed = pd.DataFrame(columns=[
            'PATIENT_ID', 'PARAM_1', 'PARAM_2', 'PARAM_3', 'PARAM_4', 'PRE_1', 'PRE_2', 'PRE_3', 'PRE_4', 'POST_1',
            'POST_2', 'POST_3', 'POST_4', 'INTERPRETATION'
        ])

    def format_general_table(self, df):
        df[['BMI', 'POIDS']] = df[['BMI', 'POIDS']].apply(lambda x: x.str.replace(',', '.'))
        df[['PATIENT_NAME', 'ETHNIE', 'SEXE']] = df[['PATIENT_NAME', 'ETHNIE', 'SEXE']].apply(lambda x: x.str.upper())
        digit_cols = ['TAILLE', 'AGE', 'BMI', 'POIDS']
        df[digit_cols] = df[digit_cols].apply(pd.to_numeric, errors='coerce')
        df['DATE_TEST'] = pd.to_datetime(df['DATE_TEST'], dayfirst=True, errors='coerce')
        return df

    def detailed_table_to_rows(self, efr_detailed_df):
        param_columns = ['PARAM_1', 'PARAM_2', 'PARAM_3', 'PARAM_4']
        transformed_rows = []

        for _, row in efr_detailed_df.iterrows():
            patient_id = row['PATIENT_ID']
            interpretation = row['INTERPRETATION']
            date_test = row['DATE_TEST']
            for param_col in param_columns:
                param = row[param_col]
                pre = row['PRE_' + param_col.split('_')[1]]
                post = row['POST_' + param_col.split('_')[1]]
                transformed_rows.append([patient_id, date_test, param, pre, post, interpretation])

        return pd.DataFrame(transformed_rows, columns=['PATIENT_ID', 'DATE_TEST', 'PARAMETRES',
                                                                       'PRE', 'POST', 'INTERPRETATION'])

    def format_detailed_rows_table(self, df):
        digital_cols = ['PRE', 'POST']
        df[digital_cols] = df[digital_cols].apply(lambda x: x.str.replace(',', '.'))
        df[digital_cols] = df[digital_cols].apply(pd.to_numeric, errors='coerce')
        df['DATE_TEST'] = pd.to_datetime(df['DATE_TEST'], dayfirst=True, errors='coerce')
        return df

    def detailed_table_to_cols(self, efr_detailed_rows_df):
        df_pivot = pd.pivot_table(efr_detailed_rows_df, index=['PATIENT_ID', 'DATE_TEST'], columns='PARAMETRES',
                                  values=['PRE', 'POST'], aggfunc='first')
        df_pivot.columns = ['_'.join(col) for col in df_pivot.columns]
        df_pivot.reset_index(inplace=True)
        df_pivot = pd.merge(df_pivot, efr_detailed_rows_df[['PATIENT_ID', 'INTERPRETATION', 'DATE_TEST']],
                            on=['PATIENT_ID', 'DATE_TEST'])
        df_pivot = df_pivot[['PATIENT_ID', 'DATE_TEST'] + [col for col in df_pivot.columns if
                                                           col not in ['PATIENT_ID', 'DATE_TEST']]]

        return df_pivot

    def format_detailed_cols_table(self, df):
        df = df.drop_duplicates()
        df = df.replace('None', np.nan)
        non_digit_cols = ["PATIENT_ID", "DATE_TEST", "INTERPRETATION"]
        digit_cols = [col for col in df.columns if col not in non_digit_cols]
        df[digit_cols] = df[digit_cols].apply(lambda x: x.str.replace(',', '.'))
        df[digit_cols] = df[digit_cols].apply(pd.to_numeric, errors='coerce')
        df['DATE_TEST'] = pd.to_datetime(df['DATE_TEST'], dayfirst=True, errors='coerce')

        # Change order of cols to begin with cols 'PRE_':
        cols_order = ["PATIENT_ID", "DATE_TEST"]
        cols_order += [col for col in df.columns if col.startswith("PRE_")]
        cols_order += [col for col in df.columns if col.startswith("POST_")]
        cols_order.append("INTERPRETATION")
        df_final = df.reindex(columns=cols_order)
        return df_final


class UniquePatientID:

    def assign_patient_id(self, patient_name, all_patients_id):
        if patient_name in all_patients_id and patient_name is not np.nan:
            patient_id = all_patients_id[patient_name]
        else:
            patient_id = uuid.uuid4()
            all_patients_id.update({patient_name: patient_id})
        return patient_id
