import os
from DataAnalyzer import DataAnalyzer
from SheetGenerator import SheetGenerator

# generate the sheets in the test directory
instance = SheetGenerator()
for i in range(10):
    instance.generate(i)

for dir, subdir, files in os.walk(r"C:\your\path"):
    for file in files:
        if dir == r"C:\your\path":
            path = dir + "\\" + file
            save_file = r"C:\your\path\{0}_descr".format(file)
            instance = DataAnalyzer(save_file, path, "Sheet1", "Date", "acct num", "MFG num", "Unit Price")
            instance.find_descr()

