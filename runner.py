import pandas as pd
from data_processing import *
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# Load and preprocess data
file_path = "/Users/jenniferrush/Python/Regis_Nursing_Analysis/data/nursing_data.xlsx"
sheet_name = "IDS - Regis College - Pre-Nursi"
raw_data = load_raw_data(file_path, sheet_name)

# Group by student
grouped_data = raw_data.groupby('Student ID#')

