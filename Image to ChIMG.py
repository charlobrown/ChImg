"""
Copyright 2025 Charlo Brown

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#---------
# Imports |
#---------
import zlib, lzma, os
from time import sleep as wait

try: # *Tries* to import Pillow.
	from PIL import Image
	from tqdm import tqdm
except Exception as exc:
	print(exc)
	exit()


#-----------------------
# Pre-defined variables |
#-----------------------
imageFile = r"image/file/path.png" # Change this to the location of your image on your computer.
maxCompCheck = 10_000
compressors = {
	1: lzma.compress,
	2: zlib.compress
}
speed = 0


#------------
# Image data |
#------------
class image:
	img = Image.open(imageFile)
	imgData = img.load()
	W, Y = img.size
	mode = img.mode
imgData = b""


#----------------------------
# Define necessary functions |
#----------------------------
def testComp(data):
	data = isBytes(data)
	checks = {}
	# Compresses the data(s) and gets the length of them in bytes.
	for compressor in compressors:
		compId = compressor
		compressor = compressors[compressor]
		checks[compId] = len(compressor(data))
		# Did I seriously contemplate if storing {maxCompData * len(compressors)} bytes into the fucking RAM was a bad idea? Of course not! No one uses 10 MB of RAM on a computer anymore! That alone can't even run Python!
	encoder = min(checks, key=checks.get) # Gets the name of the item with the smallest value in the "checks" dictionary.

	# Returns the final compressed data and the encoder ID.
	return encoder

# Checks if the data is in bytes.
def isBytes(data):
	if not isinstance(data, bytes):
		return data.encode("UTF-8")
	else:
		return data


#---------------------
# Image data creation |
#---------------------
print(f"Converting {image.mode} values to hexadecimal bytes... (May lag.)")
for i in tqdm(range(image.W * image.Y - 1)):
	try:
		wait(1 / speed)
	except:
		pass
	pixel = image.img.getpixel((
		i % image.W,
		i // image.W))
	if isinstance(pixel, tuple) or isinstance(pixel, list):
		for channel in pixel:
			imgData += bytes([channel])
			print(bytes([channel]))
	else:
		imgData += bytes([pixel])


#--------
# Finale |
#-------------------------------------
# Compression checks and writing data |
#-------------------------------------

# Caps the amount of data can be used for testing compression to reduce problems with compressing big files too many times.
if len(imgData) > maxCompCheck:
	compImgData = imgData[:maxCompCheck]
else:
	compImgData = imgData
encoder = testComp(compImgData)
compImgData = compressors[encoder](imgData)

# Metadata & file.
finalImageData = f"ChImg;;{image.mode};;{image.img.size};;{encoder}:;".encode("UTF-8")

open(os.path.join(os.path.dirname(imageFile), (os.path.basename(imageFile) + ".ChImg")), "wb").write(finalImageData + compImgData) # Writes the data to a file.


