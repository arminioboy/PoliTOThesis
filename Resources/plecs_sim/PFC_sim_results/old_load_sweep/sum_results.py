import os
import csv
import re

input_folder = "."
output_file = "results_summary.csv"

# 🔧 CONFIGURAZIONE
sort_column_name = "filename"
sort_numeric = True
sort_reverse = False

last_rows = []
header = None
sort_index = None

for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        filepath = os.path.join(input_folder, filename)
        file_base = os.path.splitext(filename)[0]

        # 🎯 Estrai solo numero iniziale (es: "123abc" → "123")
        match = re.match(r"(\d+)", file_base)
        if match:
            clean_name = match.group(1)
        else:
            continue  # salta file che non rispettano il formato

        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = list(csv.reader(f, delimiter=","))

            if not reader:
                continue

            if header is None:
                header = ["filename"] + reader[0]

                if sort_column_name not in header:
                    raise ValueError(f"Colonna '{sort_column_name}' non trovata nell'header")

                sort_index = header.index(sort_column_name)

            if len(reader) > 1:
                last_row = reader[-1]
                last_rows.append([clean_name] + last_row)

# 🔽 ORDINAMENTO
if sort_index is not None:
    if sort_numeric:
        def sort_key(row):
            try:
                return float(row[sort_index])
            except ValueError:
                return float("-inf")
    else:
        def sort_key(row):
            return row[sort_index]

    last_rows.sort(key=sort_key, reverse=sort_reverse)

# Scrittura output
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=",")
    
    if header:
        writer.writerow(header)
    
    writer.writerows(last_rows)

print(f"Creato file: {output_file}")
