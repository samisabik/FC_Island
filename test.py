import glob
import os

files_path = os.path.join(folder, '*')
files = sorted(
    glob.iglob(files_path), key=os.path.getctime, reverse=True)
print files[0]
