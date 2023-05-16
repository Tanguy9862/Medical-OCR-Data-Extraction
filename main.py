import os
import pandas as pd
from tqdm import tqdm
from PIL import Image
from Converter import ImageConverter, DocToPDF
from Extractor import Extractor, IPSExtractor, EFRExtractor
from DataManager import IPSDataManager, EFRDataManager, UniquePatientID
from Export import Export

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', None)
pd.set_option("display.max_colwidth", None)


IPS_DIRECTORY = 'E:/IPS/'
EFR_DIRECTORY = 'E:/EFR/'

image_converter = ImageConverter()
extractor = Extractor(path_to_tesseract=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
ips_extractor = IPSExtractor()
efr_extractor = EFRExtractor()
ips_data_manager = IPSDataManager()
efr_data_manager = EFRDataManager()
unique_id = UniquePatientID()
convert = DocToPDF(directory=EFR_DIRECTORY)
export = Export()

ips_general_info_df = ips_data_manager.df_general
ips_detailed_info_df = ips_data_manager.df_detailed
ips_all_files = [file for file in os.listdir(IPS_DIRECTORY) if os.path.join(IPS_DIRECTORY, file).lower().endswith('pdf')]
languages = ['FR', 'EN']
all_patients_id = {}
efr_doc_files = [file for file in os.listdir(EFR_DIRECTORY) if file.lower().endswith("doc")]
efr_pdf_files = [file for file in os.listdir(EFR_DIRECTORY) if file.lower().endswith("pdf")]
efr_general_info_df = efr_data_manager.df_general
efr_detailed_df = efr_data_manager.df_detailed
convert.convert_files(doc_files=efr_doc_files, pdf_files=efr_pdf_files)

# Extraction IPS:
# for idx, filename in tqdm(enumerate(ips_all_files), desc='[+] Extraction IPS', total=len(ips_all_files)):
#     f = os.path.join(IPS_DIRECTORY, filename)
#     # f = 'E:/IPS/2022-05-16_MYRIAMZAHRATI.pdf'
#
#     image_converter.file_to_image(file_path=f)
#     img = Image.open('IMG_0.png')
#     current_patient_data = []
#     language = extractor.detect_language(image=img)
#
#     if language in languages:
#         for item in ips_extractor.regex_roi_dict:
#             roi_image = img.crop(ips_extractor.regex_roi_dict[item]['ROI'])
#             results = extractor.extract_data_from_roi(roi_image=roi_image, item=item, language=language,
#                                                       extractor_obj=ips_extractor)
#             current_patient_data.append(results)
#             # print(f"Results: {results}")
#
#         # Check if patient is already in data:
#         PATIENT_ID = unique_id.assign_patient_id(
#             patient_name=current_patient_data[0]['PATIENT_NAME'].upper().replace(' ', ''),
#             all_patients_id=all_patients_id
#         )
#
#         # Add unique ID value and filename:
#         current_patient_data[0]['PATIENT_ID'] = PATIENT_ID
#         current_patient_data[0]['FILENAME'] = filename
#
#         # Update general info of GENERAL INFO DF:
#         ips_general_info_df.loc[
#             idx, ['FILENAME', 'PATIENT_NAME', 'PATIENT_ID', 'DATE_NAISSANCE', 'AGE', 'SEXE', 'RAPPORT_ID', 'DATE_TEST']] = [
#             current_patient_data[0]['FILENAME'],
#             current_patient_data[0]['PATIENT_NAME'],
#             current_patient_data[0]['PATIENT_ID'],
#             current_patient_data[1]['DATE_NAISSANCE'],
#             current_patient_data[1]['AGE'],
#             current_patient_data[1]['SEXE'],
#             current_patient_data[2]['RAPPORT_ID'],
#             current_patient_data[3]['DATE_TEST']
#         ]
#
#         # Add 'RAPPORT_ID' and 'DATE_TEST' column:
#         ips_general_info_df.loc[idx, 'RAPPORT_ID'] = current_patient_data[2]['RAPPORT_ID']
#         ips_general_info_df.loc[idx, 'DATE_TEST'] = current_patient_data[3]['DATE_TEST']
#
#         # Add detailed information:
#         detailed_dict = {}
#         for d in current_patient_data[4:]:
#             detailed_dict.update(d)
#         detailed_dict.update({'PATIENT_ID': PATIENT_ID, 'BORNE_INF': 1.0, 'BORNE_SUP': 1.4})
#         ips_detailed_info_df = ips_detailed_info_df._append(detailed_dict, ignore_index=True)
#         os.remove('IMG_0.png')
#
# ips_general_info_df = ips_data_manager.format_general_table(df=ips_general_info_df)
# ips_detailed_info_df = ips_data_manager.format_detailed_table(df=ips_detailed_info_df)

# Extraction EFR:
for idx, filename in tqdm(enumerate(efr_pdf_files[:1]), desc='[+] Extraction EFR', total=len(efr_pdf_files)):
    f = os.path.join(EFR_DIRECTORY, filename)
    # f = 'E:/EFR/ACHIBA _AMIROUCHE 2022_05_25 02.25.32.pdf'
    # f = 'E:/EFR/AIT EL MACHKOURI_Fatima 2015_05_28 10.26.22.pdf'
    # f = 'E:/EFR/Aberkane_Ismael 2016_05_27 16.04.31.pdf'
    print(f"Extraction {idx} | {f}")

    image_converter.file_to_image(file_path=f)
    img = Image.open('IMG_0.png')
    language = extractor.detect_language(image=img)
    current_patient_data = []

    # Création du tableau des informations générales du patient:
    if language in languages:
        for item in efr_extractor.regex_roi_dict:
            roi_image = img.crop(efr_extractor.regex_roi_dict[item]['ROI'])
            results = extractor.extract_data_from_roi(roi_image=roi_image, item=item, language=language,
                                                      extractor_obj=efr_extractor,
                                                      dotall=True if item == 'INTERPRETATION' else False)
            current_patient_data.append(results)
            # print(f"Results: {results}")
            # if item == 'GENERAL_INFORMATION' or item == 'GENERAL_INFORMATION_ADD':
            #     roi_image.show()

        # Merge of 'NOM' and 'PRENOM':
        # print(current_patient_data)
        for dict_data in current_patient_data:
            if 'NOM' in dict_data and 'PRENOM' in dict_data:
                dict_data['PATIENT_NAME'] = dict_data.pop('NOM') + ' ' + dict_data.pop('PRENOM')

        # Check if patient is already in data:
        PATIENT_ID = unique_id.assign_patient_id(
            patient_name=current_patient_data[0]['PATIENT_NAME'].upper().replace(' ', ''),
            all_patients_id=all_patients_id
        )
        current_patient_data.extend([{'FILENAME': filename}, {'PATIENT_ID': PATIENT_ID}])

        # General informations data:
        general_data = [current_patient_data[0], current_patient_data[1], current_patient_data[3],
                        current_patient_data[7], current_patient_data[8]]
        general_dict = {}
        for d in general_data:
            general_dict.update(d)
        efr_general_info_df = efr_general_info_df._append(general_dict, ignore_index=True)

        # Detailed informations data:
        detailed_dict = {}
        keys_to_extract = [2, 4, 5, 6, 8]
        for index in keys_to_extract:
            d = current_patient_data[index]
            if 'PATIENT_ID' in d:
                detailed_dict['PATIENT_ID'] = str(d['PATIENT_ID'])
            detailed_dict.update(d)
        efr_detailed_df = efr_detailed_df._append(detailed_dict, ignore_index=True)

        # Pivot data:
        id_columns = ['PATIENT_ID', 'INTERPRETATION']
        param_columns = ['PARAM_1', 'PARAM_2', 'PARAM_3', 'PARAM_4']
        transformed_rows = []

        for _, row in efr_detailed_df.iterrows():
            patient_id = row['PATIENT_ID']
            interpretation = row['INTERPRETATION']
            for param_col in param_columns:
                param = row[param_col]
                pre = row['PRE_' + param_col.split('_')[1]]
                post = row['POST_' + param_col.split('_')[1]]
                transformed_rows.append([patient_id, param, pre, post, interpretation])

        final_df = pd.DataFrame(transformed_rows, columns=['PATIENT_ID', 'PARAMETRES', 'PRE', 'POST', 'INTERPRETATION'])
        print(final_df)


# print(f'{ips_general_info_df}\n{ips_detailed_info_df}')
efr_general_info_df = efr_data_manager.format_general_table(efr_general_info_df)
efr_detailed_df = efr_data_manager.format_detailed_table(efr_detailed_df)
print(efr_general_info_df)
print(efr_detailed_df)
