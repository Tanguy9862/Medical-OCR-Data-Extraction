import pandas as pd
import xlsxwriter


class Export:

    def __init__(self):
        pass

    def export_data_to_xlsx(self, df, path, sheet_name, all_lengths: dict, has_specific_len=False):

        writer = pd.ExcelWriter(path, engine='xlsxwriter')

        # Convertir le DataFrame en feuille de calcul Excel
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Obtenir l'objet de feuille de calcul
        worksheet = writer.sheets[sheet_name]

        # Obtenir la liste des colonnes
        columns = df.columns

        # Obtenir la longueur maximale des données dans chaque colonne
        column_widths = [max(df[col].astype(str).map(len).max(), len(col)) for col in columns]

        # Définir la largeur des colonnes dans la feuille de calcul Excel
        for i, width in enumerate(column_widths):
            worksheet.set_column(i, i, width + 2)  # +2 pour un léger espacement

        if has_specific_len:
            for item in all_lengths:
                worksheet.set_column(f'{item}:{item}', all_lengths[item])

        # Enregistrer le fichier Excel
        writer._save()