# Medical OCR Data Extraction Project README

## Overview

This project aims to automate the extraction of medical data from scanned documents. It employs Optical Character Recognition (OCR) technology to read text from images and then applies regular expressions to extract specific data fields. The project is designed to handle different types of medical reports, such as IPS (Intravascular Pressure System) and EFR (Electrocardiogram Frequency Response).

## Technical Highlights

- **Languages and Libraries**: Python, NumPy, pytesseract, langdetect, re (Regular Expressions)
- **OCR Technology**: Utilizes pytesseract for OCR capabilities.
- **Language Detection**: Uses langdetect to identify the language of the text for better data extraction.
- **Regular Expressions**: Extensively uses Python's re library to match specific patterns in the OCR output.

## Features

### IPSExtractor Class

- **Region of Interest (ROI)**: Defines specific regions in the image to look for particular data fields like patient name, age, gender, etc.
- **Regular Expressions**: Utilizes different regular expressions for French and English languages to extract data.
- **Tesseract Configurations**: Allows for custom Tesseract configurations for specific data fields.

#### Data Fields Extracted:

- Patient Name
- Patient Identification Information (Date of Birth, Age, Gender)
- Report ID
- Test Date
- Intravascular Pressure System (IPS) values for both right and left
- Blood Pressure (Systolic and Diastolic)
- BPM (Beats Per Minute)

### EFRExtractor Class

- **General Information**: Extracts name, first name, ethnicity, and height from a specific ROI.
- **Additional Information**: Extracts age, gender, BMI, and weight.
- **Interpretation**: Extracts the interpretation of the test.
- **Test Parameters and Values**: Extracts various test parameters and their pre and post values.

#### Data Fields Extracted:

- Name, First Name, Ethnicity, Height
- Age, Gender, BMI, Weight
- Interpretation of the test
- Test Date
- Test Parameters and their Pre and Post values

## Challenges and Solutions

- **Language Variability**: One of the challenges was dealing with documents in multiple languages. The solution was to use langdetect to identify the language and then apply the appropriate regular expressions.
- **Complex Data Fields**: Some medical data fields required intricate regular expressions for accurate extraction. This required a deep understanding of both medical terminologies and regular expression capabilities.
- **Data Quality**: Scanned documents can have varying quality, affecting OCR performance. The project allows for custom Tesseract configurations to handle such cases.

## Skills Developed

- Mastery of OCR technologies and libraries like pytesseract.
- Advanced usage of regular expressions for data extraction.
- Experience in handling and processing image data.
- Proficiency in data cleaning and transformation.
- Understanding of medical terminologies and data fields.

## Collaboration with Medical Professionals

An integral part of this project involved regular meetings with medical professionals to discuss the relevance and importance of various data fields in medical tests. These interactions provided valuable insights into which data fields are critical for medical diagnoses and treatment plans.

## Statistical Analysis

A comprehensive RMarkdown document was created to perform statistical tests on the extracted data. The document utilizes Plotly to create interactive graphs, providing a comprehensive view of the data for better decision-making. Due to confidentiality reasons, this document is not available in this repository.
