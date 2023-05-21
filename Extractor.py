import re
import numpy as np
from pytesseract import pytesseract
from langdetect import detect


class IPSExtractor:

    def __init__(self):
        self.regex_roi_dict = {
            'PATIENT_NAME': {
                'ROI': (70, 460, 460, 560),
                'REGEX_FR': r"PATIENT\s*(?P<PATIENT_NAME>[a-zA-Z&! ]+)",
                'REGEX_EN': r"PATIENT\s*(?P<PATIENT_NAME>[a-zA-Z&! ]+)",
                'GROUP_NAMES': ['PATIENT_NAME'],
                'TESSERACT_CONFIG': None
            },
            'PATIENT_IG': {
                'ROI': (460, 460, 920, 550),
                'REGEX_FR': r"DATE DE NAISSANCE \(AGE\) SEXE\s*(?P<DATE_NAISSANCE>\d+\/\d+\/\d+\s*)?"
                            r"(?:\((?P<AGE>\d+)\))?\s*(?P<SEXE>[a-zA-Z ]+)",
                'REGEX_EN': r"DATE OF BIRTH \(AGE\) GENDER\s*(?P<DATE_NAISSANCE>\d+\/\d+\/\d+\s*)?"
                            r"(?:\((?P<AGE>\d+)\))?\s*(?P<SEXE>[a-zA-Z ]+)",
                'GROUP_NAMES': ['DATE_NAISSANCE', 'AGE', 'SEXE'],
                'TESSERACT_CONFIG': None
            },
            'RAPPORT_ID': {
                'ROI': (425, 380, 725, 445),
                'REGEX_FR': r"Rapport ID: (?P<RAPPORT_ID>[0-9A-Z]+)",
                'REGEX_EN': r"Report ID: (?P<RAPPORT_ID>[0-9A-Z]+)",
                'GROUP_NAMES': ['RAPPORT_ID'],
                'TESSERACT_CONFIG': None
            },
            'DATE_TEST': {
                'ROI': (70, 380, 400, 440),
                'REGEX_FR': r'(?P<DATE_TEST>\d+/\d+/\d+ \d+:\d+:\d+)',
                'REGEX_EN': r'(?P<DATE_TEST>\d+/\d+/\d+ \d+:\d+:\d+)',
                'GROUP_NAMES': ['DATE_TEST'],
                'TESSERACT_CONFIG': None
            },
            'IPS': {
                'ROI': (70, 570, 790, 700),
                'REGEX_FR': r"Droite: (?P<IPS_D>\d{1},\d{2}|[a-zA-Z0-9]+) Gauche: (?P<IPS_G>\d{1},\d{2}|[a-zA-Z0-9]+)",
                'REGEX_EN': r"Right: (?P<IPS_D>\d{1}.\d{2}) Left: (?P<IPS_G>\d{1}.\d{2})",
                'GROUP_NAMES': ['IPS_D', 'IPS_G'],
                'TESSERACT_CONFIG': None
            },
            'BRAS_SYS_DIA': {
                'ROI': (1280, 900, 1600, 1020),
                'REGEX_FR': r'(?i)sys\s*dia\s*(?P<BRAS_SYS>\d+|[a-zA-Z0-9]+)\s*(?P<BRAS_DIA>\d+|[a-zA-Z0-9]+)',
                'REGEX_EN': r'(?i)sys\s*dia\s*(?P<BRAS_SYS>\d+|[a-zA-Z0-9]+)\s*(?P<BRAS_DIA>\d+|[a-zA-Z0-9]+)',
                'GROUP_NAMES': ['BRAS_SYS', 'BRAS_DIA'],
                'TESSERACT_CONFIG': None
            },
            'BPM': {
                'ROI': (1425, 615, 1555, 705),
                'REGEX_FR': r"(?P<BPM>\d+|[a-zA-Z0-9]+)",
                'REGEX_EN': r"(?P<BPM>\d+|[a-zA-Z0-9]+)",
                'GROUP_NAMES': ['BPM'],
                'TESSERACT_CONFIG': None
            }
        }


class EFRExtractor:

    def __init__(self):
        self.regex_roi_dict = {
            'GENERAL_INFORMATION': {
                'ROI': (270, 395, 530, 530),
                'REGEX_FR': r'(?P<NOM>.+)\n*(?P<PRENOM>.+)\n*(?P<ETHNIE>.+)\n*(?P<TAILLE>\d+)',
                'GROUP_NAMES': ['NOM', 'PRENOM', 'ETHNIE', 'TAILLE'],
                'TESSERACT_CONFIG': '--psm 6'
            },
            'GENERAL_INFORMATION_ADD': {
                'ROI': (645, 395, 850, 530),
                'REGEX_FR': r"(?i)(?P<AGE>\d+)\n*(?P<SEXE>femme|homme)\n*(?P<BMI>\d+,\d+)\n*(?P<POIDS>\d+)",
                'GROUP_NAMES': ['AGE', 'SEXE', 'BMI', 'POIDS'],
                'TESSERACT_CONFIG': '--psm 6'
            },
            'INTERPRETATION': {
                'ROI': (50, 570, 850, 800),
                'REGEX_FR': r"(?<=Interprétation\n\n)(?P<INTERPRETATION>.*)",
                'GROUP_NAMES': ['INTERPRETATION'],
                'TESSERACT_CONFIG': None
            },
            'DATE_TEST': {
                'ROI': (50, 1080, 850, 1110),
                'REGEX_FR': r'(?i)date du test pre (?P<DATE_TEST>\d+/\d+/\d+ \d+:\d+:\d+)',
                'GROUP_NAMES': ['DATE_TEST'],
                'TESSERACT_CONFIG': None
            },
            'TESTS_PARAMETRES': {
                'ROI': (70, 880, 230, 1050),
                'REGEX_FR': r'(?i)\n*(?P<PARAM_1>[A-Z0-9%]+)\n*(?P<PARAM_2>[A-Z0-9%]+)\n*(?P<PARAM_3>[A-Z0-9%]+)\n*'
                            r'(?P<PARAM_4>[A-Z0-9%]+)',
                'GROUP_NAMES': ['PARAM_1', 'PARAM_2', 'PARAM_3', 'PARAM_4'],
                'TESSERACT_CONFIG': '--psm 6'
            },
            'TESTS_VALUES_PRE': {
                'ROI': (425, 825, 530, 1075),
                'REGEX_FR': r'(?P<PRE_1>\d+,\d+)\n*(?P<PRE_2>\d+,\d+)\n*(?P<PRE_3>\d+,\d+)\n*(?P<PRE_4>\d+,\d+)*',
                'GROUP_NAMES': ['PRE_1', 'PRE_2', 'PRE_3', 'PRE_4'],
                'TESSERACT_CONFIG': '--psm 6'
            },
            'TESTS_VALUES_POST': {
                'ROI': (635, 825, 710, 1075),
                'REGEX_FR': r'(?P<POST_1>\d+,\d+)\n*(?P<POST_2>\d+,\d+)\n*(?P<POST_3>\d+,\d+)\n*(?P<POST_4>\d+,\d+)\n*',
                'GROUP_NAMES': ['POST_1', 'POST_2', 'POST_3', 'POST_4'],
                'TESSERACT_CONFIG': '--psm 6'
            }
        }


class Extractor(IPSExtractor, EFRExtractor):

    def __init__(self, path_to_tesseract):
        super().__init__()
        pytesseract.tesseract_cmd = path_to_tesseract

    def extract_text(self, image, config):
        if config is None:
            return pytesseract.image_to_string(image)
        else:
            return pytesseract.image_to_string(image, config=config)

    def detect_language(self, image):
        return detect(self.extract_text(image, config=None)).upper()

    def extract_data_from_roi(self, roi_image, item, language, extractor_obj, dotall=False):
        regex_roi_dict = extractor_obj.regex_roi_dict
        text = self.extract_text(image=roi_image, config=regex_roi_dict[item]['TESSERACT_CONFIG'])
        if dotall:
            regex_flags = re.DOTALL
        else:
            regex_flags = 0
        match = re.search(regex_roi_dict[item][f'REGEX_{language}'], text, flags=regex_flags)
        try:
            return {name: match.group(name) for name in regex_roi_dict[item]['GROUP_NAMES']}
        except AttributeError:
            return {name: np.nan for name in regex_roi_dict[item]['GROUP_NAMES']}
