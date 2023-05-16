import pandas as pd
import uuid


class IPSDataManager:

    def __init__(self):
        self.df_general = pd.DataFrame(columns=['FILENAME', 'PATIENT_NAME', 'PATIENT_ID', 'DATE_TEST', 'RAPPORT_ID',
                                                'DATE_NAISSANCE', 'AGE', 'SEXE'])
        self.df_detailed = pd.DataFrame(columns=['PATIENT_ID', 'IPS_D', 'IPS_G', 'BPM', 'BRAS_SYS', 'BRAS_DIA',
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
        df = df.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.name != 'PATIENT_ID' else x)
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

    def format_detailed_table(self, df):
        digital_cols = ['PRE_1', 'PRE_2', 'PRE_3', 'PRE_4', 'POST_1', 'POST_2', 'POST_3', 'POST_4']
        df[digital_cols] = df[digital_cols].apply(lambda x: x.str.replace(',', '.'))
        df[digital_cols] = df[digital_cols].apply(pd.to_numeric, errors='coerce')
        return df


class UniquePatientID:

    def assign_patient_id(self, patient_name, all_patients_id):
        if patient_name in all_patients_id:
            patient_id = all_patients_id[patient_name]
        else:
            patient_id = uuid.uuid4()
            all_patients_id.update({patient_name: patient_id})
        return patient_id
