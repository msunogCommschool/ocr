from PIL import Image
from array import *


STANDARD_WIDTH = 90
STANDARD_HEIGHT = 90
# Changes the size of a given image to the standard
# Image String -> Image
def resizeToStandard(path):
	img = getImageFromPath(path)
	img = img.resize((STANDARD_WIDTH, STANDARD_HEIGHT))
	img.save(nameWithStandard(path)) 

# Returns the image at a given path, or an error if there is none
# String -> Image
def getImageFromPath(path):
	try:  
		img = Image.open(path)
		width, height = img.size
		print("width: " + str(width) + ", height: " + str(height))
		return img
	except IOError: 
		pass

# Adds Standard to the beginning of a string
# String -> String
def nameWithStandard(name):
	return "STAN" + name

# Creates a collection of data for a part of an image
# Uses a list of lists (rows, columns)
# String Int Int -> List[List[Int]]
def makeImageSection(path, xSec, ySec):
	img = Image.open(path)
	initX = 0 + (30 * xSec)
	initY = 0 + (30 * xSec)
	imgArray = []

	for i in range(0, 30):
		row = []
		for j in range(0, 30):
			row.append(img.getpixel((initX + j, initY + i)))
		imgArray.append(row)

	return imgArray



# Types of structures
# get struct types
# add...
# Then right funcs

# Creates a dictionary with values for each type of structure for a given image array
# array -> dict
def makeStructDict(array):
	imgDict = {
	"horizLine": getHorizLineVal(array)
	"horizLine": getHorizLineVal(array)
	"horizLine": getHorizLineVal(array)
	"horizLine": getHorizLineVal(array)
	"horizLine": getHorizLineVal(array) 
	}


# The following functions should all be
# List[List[Int]] -> Int (between 0 and 1)














