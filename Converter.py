from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError
import win32com.client as win32
from tqdm import tqdm
import os


class ImageConverter:

    def __init__(self, poppler_path):
        self.poppler_path = poppler_path

    def file_to_image(self, file_path):
        """
        Conversion to image format(.PNG)
        :param file_path: PDF file to convert in IMAGE format
        :return: None
        """
        try:
            images = convert_from_path(file_path, poppler_path=self.poppler_path)
        except PDFPageCountError:
            print(f'[+] Error while trying to convert {file_path}')
        else:
            for i in range(len(images)):
                images[i].save(f'IMG_{str(i)}.png', 'PNG')


class DocToPDF:

    def __init__(self, directory):
        self.word = win32.Dispatch('Word.Application')
        self.DIRECTORY = directory

    def convert_files(self, doc_files: list, pdf_files: list):
        for doc_file in tqdm(doc_files, desc='[+] Conversion fichiers .DOC -> .PDF', total=len(doc_files)):
            pdf_file = os.path.splitext(doc_file)[0] + ".pdf"
            if pdf_file in pdf_files:
                continue

            doc_path = os.path.join(self.DIRECTORY, doc_file)
            doc = self.word.Documents.Open(doc_path)
            pdf_path = os.path.join(self.DIRECTORY, pdf_file)
            doc.SaveAs(pdf_path, FileFormat=17)
            doc.Close()
            pdf_files.append(pdf_file)

        self.word.Quit()
