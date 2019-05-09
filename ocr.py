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

# *I should test the structures

# Returns an array of pixels from an image
# String -> List[List[Int]]
def imageToArrayByCol(path):
	img = Image.open(path)
	img = img.convert("L")
	imgArray = []

	for i in range(0, img.size[0]):
		col = []
		for j in range(0, img.size[1]):
			col.append(img.getpixel((i, j)))
		imgArray.append(col)

	return imgArray

# testing func
def displayColVals(path, x):
	img = Image.open(path)
	imgArray = imageToArrayByCol(path)
	for i in range(0, img.size[1]):
		print(str(imgArray[x][i]))
	return


# takes an image path and gets all the characters partitions
# String ->
def getImagePartitions(path):
	sliceIndices = [0]
	currentIndex = 0
	while nextSpaceChar(path, currentIndex) != currentIndex:
		currentIndex = nextSpaceChar(path, currentIndex)
		sliceIndices.append(currentIndex)

	for i in range(len(sliceIndices) - 1):
		cutImage(path, sliceIndices[i], sliceIndices[i + 1], i)



# Separating chars

#* shouldn't nec. be 45
# Finds x coord of the next space between characters in an image
# String int -> int
def nextSpaceChar(path, initX):

	charEnded = False
	charStarted = False
	spaces = 0
	x = initX

	imgArray = imageToArrayByCol(path)
	while x < len(imgArray):
		if columnBlank(imgArray, x):
			if charStarted:
				if not(charEnded):
					charEnded = True

				else:
					spaces = spaces + 1
		else:
			if charEnded:
				return x - (spaces // 2)
			else:
				charStarted = True
		x = x + 1
	print(str(spaces))
	return x - (spaces // 2)

"""
# Cuts an image at a given column and returns that array
# String Int -> List[List[Int]]
def cutImage(path, x):
	imgArray = imageToArrayByCol(path)
	newArray = imgArray[:x]
"""

def cutImage(path, xStart, xEnd, i):
	img = Image.open(path)
	img.crop((xStart, 0, xEnd, img.size[1])).save((path[:(len(path) - 4)] + str(i) + ".png"))
	#return img.crop((xStart, 44, xEnd, 0))

# Checks if an image is blank ata given column
# List[List[Int]] Int -> Bool
def columnBlank(array, x):
	column = array[x]
	for y in array[x]:
		if y < 200:
			return False
	return True

			



















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

"""
#***This Shouldn't return 0 easily.
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

	# Adding .1 t return value
	# To fix mistake of 0 trumping, obv not a permanent solution.
	return (sqrt(.04 * nonWhiteCount)) + .1
"""

#***This Shouldn't return 0 easily.
# Returns a value based on how percentage of non-white pixels in 5x5 block
# Returns a value between 0 and 1
# Uses sqrt(.04*x) for 0 <= x <= 25
# List[List[Int]] -> Int

STARTING_COUNT = 3.0

def evalBlock(array):
	nonWhiteCount = STARTING_COUNT
	for row in array:
		for pixel in row:
			if (pixel < 255):
				nonWhiteCount = nonWhiteCount + ((25.0 - STARTING_COUNT) / 25.0)

	# To fix mistake of 0 trumping, obv not a permanent solution.
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


# Returns a list of the structure evaluation dictionaries
# (The top level)
# String -> List[Dict[String -> int]]
def getImageStructureEvals(path):
	evalList = []
	for i in range(0, 3):
		for j in range(0, 3):
			structure = makeImageSection(path, j, i)
			evalList.append(makeStructDict(structure))

	return evalList


# Creates a dictionary with values for each type of structure for a given image array
# maybe switch to class
# array -> dict

def makeStructDict(array):
	imgDict = {
		"horizLine": horizLineVal(array),
		"vertLine": vertLineVal(array),
		"leftDiag": leftDiagLineVal(array),
		"rightDiag": rightDiagLineVal(array),
		"leftUp": leftUpCurveVal(array),
		"leftDown": leftDownCurveVal(array),
		"rightUp": rightUpCurveVal(array),
		"rightDown": rightDownCurveVal(array),
		"blank": blankVal(array) 
	}

	return imgDict


# The following functions should all be
# List[List[Int]] -> Int (between 0 and 1)
# Make these return nth rooth

def horizLineVal(array):
	evalList = getStructureSectionEvals(array)

	topLine = (evalList[0] * evalList[1] * evalList[2])**(1.0/3)
	midLine = (evalList[3] * evalList[4] * evalList[5])**(1.0/3)
	botLine = (evalList[6] * evalList[7] * evalList[8])**(1.0/3)

	return max(topLine, midLine, botLine)

def vertLineVal(array):
	evalList = getStructureSectionEvals(array)

	leftLine = (evalList[0] * evalList[3] * evalList[6])**(1.0/3)
	midLine = (evalList[2] * evalList[5] * evalList[7])**(1.0/3)
	rightLine = (evalList[3] * evalList[6] * evalList[8])**(1.0/3)

	return max(leftLine, midLine, rightLine)

def leftDiagLineVal(array):
	evalList = getStructureSectionEvals(array)

	line = (evalList[6] * evalList[4] * evalList[2])**(1.0/3)

	return line

def rightDiagLineVal(array):
	evalList = getStructureSectionEvals(array)

	line = (evalList[0] * evalList[4] * evalList[8])**(1.0/3)

	return line

def leftUpCurveVal(array):
	evalList = getStructureSectionEvals(array)

	topLine = (evalList[3] * evalList[4] * evalList[1] * (1 - evalList[0]))**(1.0/4)
	botLine = (evalList[7] * evalList[8] * evalList[5] * (1 - evalList[0]))**(1.0/4)

	return max(topLine, botLine)

#Can I standardize all of these, 4 of these.
def leftDownCurveVal(array):
	evalList = getStructureSectionEvals(array)

	topLine = (evalList[3] * evalList[4] * evalList[7] * (1 - evalList[6]))**(1.0/4)
	botLine = (evalList[1] * evalList[2] * evalList[5] * (1 - evalList[6]))**(1.0/4)

	return max(topLine, botLine)

def rightUpCurveVal(array):
	evalList = getStructureSectionEvals(array)

	topLine = (evalList[1] * evalList[4] * evalList[5] * (1 - evalList[2]))**(1.0/4)
	botLine = (evalList[3] * evalList[6] * evalList[7] * (1 - evalList[2]))**(1.0/4)

	return max(topLine, botLine)

def rightDownCurveVal(array):
	evalList = getStructureSectionEvals(array)

	topLine = (evalList[3] * evalList[0] * evalList[1] * (1 - evalList[8]))**(1.0/4)
	botLine = (evalList[7] * evalList[4] * evalList[5] * (1 - evalList[8]))**(1.0/4)

	return max(topLine, botLine)

def blankVal(array):
	evalList = getStructureSectionEvals(array)

	block = ((1 - evalList[0]) * (1 - evalList[1]) * (1 - evalList[2]) * (1 - evalList[3])
	 * (1 - evalList[4]) * (1 - evalList[5]) * (1 - evalList[6]) * (1 - evalList[7])
	 * (1 - evalList[8]))**(1.0/10)

	return block



# Character Structure Dictionaries
# pair characters to lists
# lists containging lists of structure types

charStructDict = {
	"a": [["rightDown", "horizLine", "vertLine", "vertLine", "", "vertLine", "rightUp", "horizLine", "vertLine"]],
	"b": [["vertLine", "", "", "vertLine", "horizLine", "leftDown", "vertLine", "horizLine", "leftUp"]],	
	"c": [["rightDown", "horizLine", "", "vertLine", "", "", "rightUp", "horizLine", ""]],
	"d": [["", "", "vertLine", "rightDown", "horizLine", "vertLine", "rightUp", "horizLine", "vertLine"]],
	"e": [["rightDown", "horizLine", "leftDown", "horizLine", "horizLine", "horizLine", "rightDown", "horizLine", ""]],
	
	"f": [["", "rightDown", "horizLine", "horizLine", "vertLine", "horizLine", "", "vertLine", ""]],
	"g": [["rightDown", "horizLine", "vertLine", "vertLine", "", "vertLine", "", "horizLine", "leftUp"]],	
	"h": [["vertLine", "", "", "vertLine", "horizLine", "leftDown", "vertLine", "", "vertLine"]],
	#* "i": [["", "", "vertLine", "rightDown", "horizLine", "vertLine", "rightUp", "horizLine", "vertLine"]],
	"j": [["", "vertLine", "", "", "vertLine", "", "leftUp", "vertLine", ""]],

	"k": [["vertLine", "", "", "vertLine", "leftDiag", "", "vertLine", "rightDiag", ""]],
	#(*) "l": [["", "vertLine", "", "", "vertLine", "", "", "vertLine", ""]],	
	"m": [["horizLine", "horizLine", "horizLine", "vertLine", "vertLine", "vertLine", "vertLine", "vertLine", "vertLine"]],
	"n": [["rightDown", "horizLine", "leftDown", "vertLine", "", "vertLine", "vertLine", "", "vertLine"]],
	# it's 0, ... "o": [["rightDown", "horizLine", "leftDown", "vertLine", "", "vertLine", "rightUp", "horizLine", "leftUp"]],

	"p": [["vertLine", "horizLine", "leftDown", "vertLine", "horizLine", "leftUp", "vertLine", "", ""]],
	"q": [["rightDown", "horizLine", "vertLine", "rightUp", "horizLine", "vertLine", "", "", "vertLine"]],	
	# bad "r": [["vertLine", "", "", "vertLine", "horizLine", "", "vertLine", "", ""]],
	"s": [["vertLine", "horizLine", "", "rightUp", "rightDiag", "leftDown", "", "horizLine", "vertLine"]],
	
	"u": [["vertLine", "", "vertLine", "vertLine", "", "vertLine", "rightUp", "horizLine", "leftUp"]],

	# bad "v": [["rightDiag", "", "leftDiag", "rightDiag", "", "leftDiag", "", "", ""]],
	# "w": [["rightDiag", "", "leftDiag", "vertLine", "horizLine", "leftDown", "vertLine", "horizLine", "leftUp"]],	
	"x": [["rightDiag", "", "leftDiag", "", "", "", "leftDiag", "", "rightDiag"]],
	"y": [["rightDiag", "", "leftDiag", "", "leftDiag", "", "leftUp", "", ""]],
	"z": [["horizLine", "horizLine", "leftDiag", "", "leftDiag", "", "leftDiag", "horizLine", "horizLine"]],

	"t": [["horizLine", "vertLine", "horizLine", "", "vertLine", "", "", "vertLine", ""],
	["", "vertLine", "", "horizLine", "vertLine", "horizLine", "", "vertLine", ""]],
	"1": [["vertLine", "", "", "vertLine", "", "", "vertLine", "", ""],
	["", "vertLine", "", "", "vertLine", "", "vertLine", "", ""],
	["", "", "vertLine", "", "", "vertLine", "", "", "vertLine"]],
	"0": [["rightDown", "horizLine", "leftDown", "vertLine", "", "vertLine", "rightUp", "horizLine", "leftUp"]]
}

# Prints the top 5 most likely characters for a given image
# String ->
def topFiveChars(path):
	topCharsAndValues = []
	for char in charStructDict:
		print(char + ": ")
		print(str(charProbability(path, char)) + "\n")



# Given an image path, returns the probability that it is a given char
# String String -> Int
def charProbability(path, char):
	dicts = getImageStructureEvals(path)
	return charProbabilityFromDicts(dicts, char)


# Given a structure array, returns the probability that it is a given char
# List[Dict[String -> int]] String -> Int
def charProbabilityFromDicts(dict, char):
	checkDicts = charStructDict[char]

	max = 0
	for checkDict in checkDicts:
		if dictAffinity(dict, checkDict) > max:
			max = dictAffinityWithWhite(dict, checkDict)
	return max

# Returns how strong two dicts match
# List[Dict[String -> int]] List[String] Int -> Int
def dictAffinity(dict, matches):
	affinity = 1
	mult = 0
	for i in range(9):
		if matches[i] != "":
			mult = mult + 1
			affinity = affinity * dict[i][matches[i]]

	return affinity ** (1.0/float(mult))


# Returns how strong two dicts match using white space
# List[Dict[String -> int]] List[String] Int -> Int
def dictAffinityWithWhite(dict, matches):
	affinity = 1
	for i in range(8):
		if matches[i] == "":
			affinity = affinity * dict[i]["blank"]
		else:
			affinity = affinity * dict[i][matches[i]]

	return affinity ** (1.0/9)








"""
left up: 3, 4, 1 | 7, 8, 5 (0)
left down: 3, 4, 7 | 1, 2, 5 (6)
right up: 1, 4, 5 | 3, 6, 7 (2)
**right down: 3, 0, 1 | 7, 4, 5 ()
find a func

# possibly standardiation
# horiz and vert strings left right, up down.
def curveVal(array, horiz, vert):

	if horiz == left:

	topLine = (evalList[a] * evalList[b] * evalList[c] * (1 - evalList[d]))**(1.0/4)
	botLine = (evalList[e] * evalList[f] * evalList[g] * (1 - evalList[d]))**(1.0/4)
"""













