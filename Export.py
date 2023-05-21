import pandas as pd
import xlsxwriter
from tqdm import tqdm

class Export:

    def __init__(self):
        pass

    def create_xlsx(self, df, path, sheet_name, all_lengths: dict, has_specific_len):
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        worksheet = writer.sheets[sheet_name]
        columns = df.columns
        column_widths = [max(df[col].astype(str).map(len).max(), len(col)) for col in columns]

        # Define width column in Excel sheet:
        for i, width in enumerate(column_widths):
            worksheet.set_column(i, i, width + 2)  # +2 pour un léger espacement

        if has_specific_len:
            for item in all_lengths:
                worksheet.set_column(f'{item}:{item}', all_lengths[item])

        writer._save()

    def export_data(self, all_dfs):
        for df in tqdm(all_dfs, desc='[+] Export', total=len(all_dfs)):

            if all_dfs[df][1] is True:
                has_specific_len = True
                defined_length = all_dfs[df][2]
            else:
                has_specific_len = False
                defined_length = {}

            self.create_xlsx(
                df=all_dfs[df][0],
                path=f"Export/{df.split('_')[0]}/{df}.xlsx",
                sheet_name=df,
                has_specific_len=has_specific_len,
                all_lengths=defined_length
            )
