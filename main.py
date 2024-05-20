import fitz  # PyMuPDF
import pandas as pd

import argparse
from pathlib import Path

def extract_table_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    table_data = []

    text = ""
    for page_num in range(len(doc)):
        
        page = doc.load_page(page_num)
        text += page.get_text("text")

    lines = text.split("\n")
    
    filtered = []
    skip = False
    for i in range(len(lines)):
        line = lines[i]
        if "mit Erfolg" in line:
            filtered.append(line + lines[i+1])
            skip = True
        elif skip:
            skip = False
            continue
        else:
            
            filtered.append(line)
            
    lines = filtered
    active = False
    thesis = False
    exam = False
    for i in range(len(lines)):
        line = lines[i]

        if "LVA - Prüfungen" in line:
            active = True
            continue

        if (
            "Linz, am" in line 
            or "Kumulative Fachprüfungen" in line 
            or "Fachprüfung in Form einer Lehrveranstaltungsprüfung" in line
            or "Freie Studienleistungen" in line
            or "Gesamtprüfung" in line
            or "Masterarbeit" in line
            or "Kommissionelle Prüfungen" in line
        ):
            active = False
            

        if active:
            table_data.append(line)

        if "Masterarbeit" in line: 
            # parse with empty spots
            thesis = True
            table_data.extend([
                lines[i+1], # name
                None, # type
                lines[i+2], # ects
                None, # SWS
                lines[i+4], # date,
                lines[i+5], # grade,
                lines[i+6], # prof,
                None, # id1
                None, # id2
            ])
        elif "Kommissionelle Prüfungen" in line: 
            for j in range(3):
                # parse with empty spots
                table_data.extend([
                    lines[i+1], # name
                    None, # type
                    lines[i+2], # ects
                    None, # SWS
                    lines[i+4], # date,
                    lines[i+5], # grade,
                    lines[i+6], # prof,
                    None, # id1
                    None, # id2
                ])
                i += 6



    table = []
    while table_data:
        table.append(table_data[:9])
        table_data = table_data[9:]

    df = pd.DataFrame(table, columns=["name", "type", "ects", "sws", "date", "grade", "prof", "id", "code"])
    df = df.drop(["name", "type", "sws", "date", "prof", "id", "code"], axis=1)
    df = df[df["grade"] != "mit Erfolgteilgenommen"]
    mapping = {'sehr gut':1, 'gut':2, 'befriedigend' : 3, 'genügend' : 4}
    df['ects'] = df['ects'].astype(float)
    df['grade'] = df['grade'].replace(mapping)

    ects_weighted_grade = (df['grade'] * df['ects']).sum() /  df['ects'].sum()

    return ects_weighted_grade


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help='The name of the file to check.')

    # Parse the arguments
    args = parser.parse_args()

    # Convert the filename to a Path object
    file_path = Path(args.filename)

    # Check if the file exists
    if not file_path.exists():
        print(f"The file '{file_path}' does not exist.")
        return

    ects_weighted_grade = extract_table_from_pdf(file_path)
    print("ECTS weigthed grade: ", ects_weighted_grade)

if __name__ == "__main__":
    main()
