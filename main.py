import os
from sc_compression import decompress
import struct

input_dir = "./input"
output_dir = "./output"

if not os.path.exists(input_dir):
	os.makedirs(input_dir)
	quit()
if not os.path.exists(output_dir):
	os.makedirs(output_dir)
	quit()

def dec(file):
	file = file[:-3]
	with open(f'./{file}.sc', 'rb') as f:
		data = f.read()
	if b"START" in data:
		data = data.split(b"START")[0]
	with open(f'./{file}_decoded.sc', 'wb') as f:
		f.write(decompress(data)[0])
		
for filename in os.listdir(input_dir):
	if filename.endswith(".sc"):
		if not filename.endswith("_tex.sc"):
			input_path = os.path.join(input_dir, filename)
			dec(input_path)
			decfilepath = os.path.join(input_dir, filename[:-3]+"_decoded.sc")
			exportnames = []
			with open(decfilepath, "rb") as file:
				offset = 17
				file.seek(offset)
				exportCount = struct.unpack('<H', file.read(2))[0]
				offset += exportCount * 2 + 2 
				for i in range(exportCount):
					file.seek(offset)
					exportlength = struct.unpack('<B', file.read(1))[0]
					offset += 1
					file.seek(offset)
					exportnames.append(file.read(exportlength).decode('utf-8'))
					offset += exportlength
				out = os.path.join(output_dir, os.path.basename(filename)[:-2]+"txt")
				with open(out, "w", encoding="utf-8") as f:
					for i in exportnames:
						f.write(i+"\n")
				print(f"Succesfully exported {exportCount} exportnames from {filename}")
			os.remove(decfilepath)
print("Done!")
os.system("pause")
