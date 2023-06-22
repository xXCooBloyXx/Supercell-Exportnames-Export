import os
import re

input_dir = "./input"
output_dir = "./output"

if not os.path.exists(input_dir):
    os.makedirs(input_dir)
    quit()
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    quit()

def extract_export_names(data):
    export_names = []
    i = data.find(b"START") + 5
    while i < len(data):
        export_name = ""
        j = i
        while j < len(data) and data[j] != 0:
            export_name += chr(data[j])
            j += 1
        if len(export_name) > 0:
            export_names.append(export_name)
        if j == len(data):
            break
        i = j + 18
        if i < len(data):
            next_char = chr(data[i])
            if not re.match(r"[a-z0-9_]", next_char):
                break
    return export_names

for filename in os.listdir(input_dir):
    input_path = os.path.join(input_dir, filename)
    with open(input_path, "rb") as input_file:
        input_data = input_file.read()
        export_names = extract_export_names(input_data)
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, "w", encoding="utf-8") as output_file:
            for export_name in export_names:
                output_file.write(export_name + "\n")
            line_count = len(export_names)
            print(f"Successfully exported {line_count} export names from {filename}!")
print("Done!")
os.system("pause")
