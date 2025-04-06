import argparse
import os
import pandas as pd

def export_sheet_to_csv(input_xlsx, output_csv, sheet_name):
    # Load the specified sheet from the XLSX file
    df = pd.read_excel(input_xlsx, sheet_name=sheet_name)   
    # Save the DataFrame to a CSV file
    df.to_csv(output_csv, index=False, sep='\t')
    print(f"Exported {sheet_name} to {output_csv}")

argparser = argparse.ArgumentParser(description='Export a selected sheet from an XLSX file to a CSV file.')
argparser.add_argument('input_xlsx', type=str, help='The input XLSX file to process')
argparser.add_argument('output_csv', type=str, help='The output CSV file to process')
argparser.add_argument('--sheet', type=str, help='The name of the sheet to export')
args = argparser.parse_args()

xls = pd.ExcelFile(args.input_xlsx)

if args.sheet:
    # If a specific sheet name is provided, export that sheet
    export_sheet_to_csv(args.input_xlsx, args.output_csv, args.sheet)
else:
    # If no specific sheet name is provided, export all sheets
    for sheet_name in xls.sheet_names:
        output_csv = os.path.splitext(args.output_csv)[0] + f"_{sheet_name}.csv"
        export_sheet_to_csv(args.input_xlsx, output_csv, sheet_name)