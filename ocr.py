from PIL import Image
from array import *
from math import sqrt


STANDARD_WIDTH = 45
STANDARD_HEIGHT = 45
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
	initX = 0 + (15 * xSec)
	initY = 0 + (15 * xSec)
	imgArray = []

	for i in range(0, 15):
		row = []
		for j in range(0, 15):
			row.append(img.getpixel((initX + j, initY + i)))
		imgArray.append(row)

	return imgArray



# Creates a collection of data for a section of an structure array
# Uses a list of lists (rows, columns)
# List[List[Int]] Int Int -> List[List[Int]]
def makeStructureSection(array, xSec, ySec):
	initX = 0 + (5 * xSec)
	initY = 0 + (5 * xSec)
	structArray = []

	for i in range(0, 5):
		row = []
		for j in range(0, 5):
			row.append(array[initY + j][initX + i])
		structArray.append(row)

	return structArray	


# Should I use a third layer?

# Returns the value of a pixel of a given image array
# List[List[Int]] Int Int -> Int
def pixelAtPos(array, x, y):
	return array[y][x]



# Returns a value based on how percentage of non-white pixels in 5x5 block
# Returns a value between 0 and 1
# Uses sqrt(.04*x) for 0 <= x <= 25
# List[List[Int]] -> Int
def evalBlock(array):
	nonWhiteCount = 0
	for row in array:
		for pixel in row:
			if (pixel > 0):
				nonWhiteCount = nonWhiteCount + 1

	return (sqrt(.04 * nonWhiteCount))

# Returns a list of the structure section evaluations
# List[List[Int]] -> List[Int]
def getStructureSectionEvals(array):
	evalList = []
	for i in range(0, 3):
		for j in range(0, 3):
			section = makeStructureSection(array, j, i)
			evalList.append(evalBlock(section))

	return evalList



# Creates a dictionary with values for each type of structure for a given image array
# array -> dict
"""
def makeStructDict(array):
	imgDict = {
	"horizLine": getHorizLineVal(array)
	"horizLine": getHorizLineVal(array)
	"horizLine": getHorizLineVal(array)
	"horizLine": getHorizLineVal(array)
	"horizLine": getHorizLineVal(array) 
	}

	return imgDict
"""
# The following functions should all be
# List[List[Int]] -> Int (between 0 and 1)


def getHorizLineVal(array):
	evalList = getStructureSectionEvals(array)

	topLine = evalList[0] * evalList[1] * evalList[2]
	midLine = evalList[3] * evalList[4] * evalList[5]
	botLine = evalList[6] * evalList[7] * evalList[8]

	return max(topLine, midLine, botLine)











