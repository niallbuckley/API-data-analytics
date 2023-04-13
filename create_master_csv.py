import os
import glob
import pandas as pd
import numpy as np

csv_dir = './results'

csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))

merged_data = pd.DataFrame()

seen_files = set()

try:
    with open('seen.txt', 'r') as file:
        for line in file:
            seen_files.add(line.strip())
except FileNotFoundError:
    open('seen.txt', 'w').close()


# Loop through each csv file and append its data to the merged data DataFrame
for csv_file in csv_files:
    if os.path.basename(csv_file) in seen_files:
        print (f"Skipping {csv_file} - already seen!")
        continue
    data = pd.read_csv(csv_file)
    merged_data = merged_data.append(data, ignore_index=True)
    seen_files.add(os.path.basename(csv_file))
    break

# Save the merged data to the master CSV file
merged_data.to_csv('./results/master_file.csv', index=False)

with open('seen.txt', 'w') as file:
    for f in seen_files:
        file.write(f"{f}\n")
