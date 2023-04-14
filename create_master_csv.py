import os
import glob
import pandas as pd

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

dfs = []

# Loop through each csv file and append its data to the merged data DataFrame
for csv_file in csv_files:
    if os.path.basename(csv_file) in seen_files:
        print (f"Skipping {csv_file} - already seen!")
        continue
    print (f"Processing {csv_file}")
    one_run = pd.read_csv(csv_file)
    dfs.append(one_run)
    seen_files.add(os.path.basename(csv_file))

combined_df = pd.concat(dfs)

# Save the merged data to the master CSV file
combined_df.to_csv('./results/master_file.csv', index=False)

with open('seen.txt', 'w') as file:
    for f in seen_files:
        file.write(f"{f}\n")
