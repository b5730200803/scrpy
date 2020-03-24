import pandas as pd
import numpy as np
from openpyxl import load_workbook

path = r"C:\Users\MiniPair\Desktop\PhD_data.xlsx"

book = load_workbook(path)
writer = pd.ExcelWriter(path, engine = 'openpyxl')
writer.book = book

x3 = np.random.randn(100, 2)
df3 = pd.DataFrame(x3)

x4 = np.random.randn(100, 2)
df4 = pd.DataFrame(x4)

df3.to_excel(writer, sheet_name = 'x3')
df4.to_excel(writer, sheet_name = 'x4')
writer.save()
writer.close()