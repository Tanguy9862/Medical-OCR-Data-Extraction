# Medical OCR Data Extraction

Automated the extraction of medical data from scanned documents using **Optical Character Recognition (OCR)** and regular expressions, enabling efficient data processing and analysis.

## 📄 Overview
This project focuses on automating the extraction of medical data from scanned documents. By leveraging OCR technology, the script reads text from images and applies regular expressions to extract specific data fields. It is designed to handle various types of medical reports, such as IPS (Intravascular Pressure System) and EFR (Electrocardiogram Frequency Response).

## 🛠️ Technical Highlights

- **Programming Language:** Python
- **Libraries:**
  - ```pytesseract```
  - ```Pandas```
  - ```NumPy```
  - ```langdetect```
  - ```re```
- **Reporting:** RMarkdown

## 🧰 Challenges and Solutions

- **Language Variability**: One of the challenges was dealing with documents in multiple languages. The solution was to use langdetect to identify the language and then apply the appropriate regular expressions.
- **Complex Data Fields**: Some medical data fields required intricate regular expressions for accurate extraction. This required a deep understanding of both medical terminologies and regular expression capabilities.
- **Data Quality**: Scanned documents can have varying quality, affecting OCR performance. The project allows for custom Tesseract configurations to handle such cases.

## 👨‍⚕️ Collaboration and Statistical Analysis

This project involved regular collaboration with medical professionals to identify and prioritize critical data fields relevant for medical diagnoses and treatment plans. Their expertise guided the selection of key metrics to focus on during data extraction and analysis. A comprehensive RMarkdown document was also developed to perform statistical tests on the extracted data, featuring interactive graphs powered by Plotly to aid decision-making. Due to confidentiality, the RMarkdown file is not included in this repository.
