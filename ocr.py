from PIL import Image
from array import *
from math import sqrt


#
# Gathering and standardizing data
#

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

STANDARD_WIDTH = 45
STANDARD_HEIGHT = 45
# Changes the size of a given image to the standard
# Image String -> Image
def resizeToStandard(path):
	img = getImageFromPath(path)
	img = img.resize((STANDARD_WIDTH, STANDARD_HEIGHT))
	img.save(nameWithStandard(path)) 

# Make an image black and white
# String ->
def makeBW(path):
	image = Image.open(path)
	image = image.convert('1') # convert image to black and white
	image.save(nameWithBW(path))


# Adds STAN to the beginning of a string
# String -> String
def nameWithStandard(name):
	return "STAN" + name

# Adds BW to the beginning of a string
# String -> String
def nameWithBW(name):
	return "BW" + name


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


# Converts an array by columns to an array by rows
# List[List[Int]] -> List[List[Int]]
def arrayByColToRow(array):
	imgArray = []

	for i in range(len(array[0])):
		row = []
		for j in range(len(array)):
			row.append(array[j][i])
		imgArray.append(row)

	return imgArray


# Testing func for above
# Displays values for a column of pixels from an image
# String Int ->
def displayColVals(path, x):
	img = Image.open(path)
	imgArray = imageToArrayByCol(path)
	for i in range(0, img.size[1]):
		print(str(imgArray[x][i]))
	return



			

#
# Following functions break up the image
#

# To break up full image into 9 sections (3x3 grid of 15x15 pix)

# Creates a collection of data for a part of an image
# Uses a list of lists (rows, columns)
# String Int Int -> List[List[Int]]
def makeImageSection(path, xSec, ySec):
	img = Image.open(path)
	initX = 0 + (15 * xSec)
	initY = 0 + (15 * (2 - ySec))
	imgArray = []

	for i in range(0, 15):
		col = []
		for j in range(0, 15):
			col.append(img.getpixel((initX + i, initY + j)))
		imgArray.append(col)

	return imgArray



# To break up section into 9 structure blocks (3x3 grid of 5x5 pix)

# Creates a collection of data for a section of an structure array
# Uses a list of lists (rows, columns)
# List[List[Int]] Int Int -> List[List[Int]]
def makeStructureSection(array, xSec, ySec):
	initX = 0 + (5 * xSec)
	initY = 0 + (5 * (2 - ySec))
	structArray = []

	for i in range(0, 5):
		col = []
		for j in range(0, 5):
			col.append(array[initX + i][initY + j])
		structArray.append(col)

	return structArray	


# Returns the value of a pixel of a given image array
# List[List[Int]] Int Int -> Int
def pixelAtPos(array, x, y):
	return array[x][y]




#
# Following functions evaluate images/image sections
#

# Evaluate a structure block (3rd layer)


STARTING_COUNT = .2

# Returns a value based on how percentage of non-white pixels in 5x5 block
# Returns a value between 0 and .987
# (Cannot return 0 or 1 due to errors when taking roots of these values)
# List[List[Int]] -> Int
def evalBlock(array):
	nonWhiteCount = STARTING_COUNT
	for col in array:
		for pixel in col:
			if (pixel > 0):
				nonWhiteCount = nonWhiteCount + ((25.0 - STARTING_COUNT) / 25.0)
	return ((.039 * nonWhiteCount)**(1/2.0))






# Evaluate a section (2nd layer)

# Returns a list of the structure section evaluations
# List[List[Int]] -> List[Int]
def getStructureSectionEvals(array):
	evalList = []
	for j in range(0, 3):
		for i in range(0, 3):
			section = makeStructureSection(array, i, j)
			evalList.append(evalBlock(section))

	return evalList








# The following functions should all be
# List[List[Int]] -> Int (between 0 and 1)
# Make these return nth rooth

# These could take into account the blanks. 

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


# bias toward blank because all structures contain some blankness.
# Fix with this <1 exponent multipler
BLANK_SCALE = (1.0/3)
def blankVal(array):
	evalList = getStructureSectionEvals(array)

	block = ((1 - evalList[0]**BLANK_SCALE) * (1 - evalList[1]**BLANK_SCALE) * (1 - evalList[2]**BLANK_SCALE)
	 * (1 - evalList[3]**BLANK_SCALE) * (1 - evalList[4]**BLANK_SCALE) * (1 - evalList[5]**BLANK_SCALE)
	 * (1 - evalList[6]**BLANK_SCALE) * (1 - evalList[7]**BLANK_SCALE) * (1 - evalList[8]**BLANK_SCALE))**(1.0/10)

	return block







# Evaluate an image (1st layer) by structures

# Returns a list of the structure evaluation dictionaries
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


# These functions take into account white space for structure evaluations


"""


# The following functions should all be
# List[List[Int]] -> Int (between 0 and 1)
# Make these return nth rooth

# These could take into account the blanks. 

def structureVal(array, blockList):
	maxVal = 0
	evalList = getStructureSectionEvals(array)

	for blocks in blockList:
		val = 1
		listIndex = 0
		for block in range(9):
			if len(blocks) > listIndex:
				if block == blocks[listIndex]:
					val = val * evalList[block]
					listIndex = listIndex + 1
				else:
					val = val * (1 - evalList[block])
			else:
				val = val * (1 - evalList[block])
		if val > maxVal:
			maxVal = val
	return maxVal

def makeStructDict(array):
	imgDict = {
		"horizLine": structureVal(array, [[0, 1, 2], [3, 4, 5], [6, 7, 8]]),
		"vertLine": structureVal(array, [[0, 3, 6], [1, 4, 7], [2, 5, 8]]),
		"leftDiag": structureVal(array, [[2, 4, 6]]),
		"rightDiag": structureVal(array, [[0, 4, 8]]),
		"leftUp": structureVal(array, [[1, 3, 4], [5, 7, 8]]),
		"leftDown": structureVal(array, [[3, 4, 7], [1, 2, 5]]),
		"rightUp": structureVal(array, [[1, 4, 5], [3, 6, 7]]),
		"rightDown": structureVal(array, [[0, 1, 3], [4, 5, 7]]),
		"blank": blankVal(array) 
	}

	return imgDict


"""











# Evaluate an image (1st layer) and return result

# Prints the top 5 most likely characters for a given image
# String ->
def topFiveChars(path):
	topCharsAndVals = []
	for char in charStructDict:
		if len(topCharsAndVals) < 5:
			topCharsAndVals.append((char, charProbability(path, char)))
		else:
			topCharsAndVals.sort(key=lambda tup: tup[1])
			if charProbability(path, char) > topCharsAndVals[0][1]:
				topCharsAndVals[0] = (char, charProbability(path, char))
	topCharsAndVals.sort(key=lambda tup: tup[1])
	for tup in topCharsAndVals:
		print(tup[0])



# Prints all char probabilities
# String ->
def allCharProbabilities(path):
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
		if dictAffinityWithWhite(dict, checkDict) > max:
			max = dictAffinityWithWhite(dict, checkDict)
	return max

# Returns how strong two dicts match
# This function doesn't use empty space as a structure type
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
	for i in range(9):
		if matches[i] == "":
			affinity = affinity * dict[i]["blank"]
		else:
			affinity = affinity * dict[i][matches[i]]

	return affinity ** (1.0/9)



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
	"i": [["", "", "", "vertLine", "", "", "vertLine", "", ""],
	["", "", "", "", "vertLine", "", "", "vertLine", ""],
	["", "", "", "", "", "vertLine", "", "", "vertLine"]],
	"j": [["", "vertLine", "", "", "vertLine", "", "leftUp", "vertLine", ""]],

	"k": [["vertLine", "", "", "vertLine", "leftDiag", "", "vertLine", "rightDiag", ""]],
	"l": [["vertLine", "", "", "vertLine", "", "", "vertLine", "", ""],
	["", "vertLine", "", "", "vertLine", "", "", "vertLine", ""],
	["", "", "vertLine", "", "", "vertLine", "", "", "vertLine"]],	
	"m": [["horizLine", "horizLine", "horizLine", "vertLine", "vertLine", "vertLine", "vertLine", "vertLine", "vertLine"]],
	"n": [["rightDown", "horizLine", "leftDown", "vertLine", "", "vertLine", "vertLine", "", "vertLine"]],
	"o": [["rightDown", "horizLine", "leftDown", "vertLine", "", "vertLine", "rightUp", "horizLine", "leftUp"]],

	"p": [["vertLine", "horizLine", "leftDown", "vertLine", "horizLine", "leftUp", "vertLine", "", ""]],
	"q": [["rightDown", "horizLine", "vertLine", "rightUp", "horizLine", "vertLine", "", "", "vertLine"]],	
	"r": [["vertLine", "", "", "vertLine", "rightDown", "", "vertLine", "horizLine", ""],
	["", "vertLine", "", "", "vertLine", "rightDown", "", "vertLine", "horizLine"]],
	"s": [["vertLine", "horizLine", "", "rightUp", "rightDiag", "leftDown", "", "horizLine", "vertLine"]],
	
	"u": [["vertLine", "", "vertLine", "vertLine", "", "vertLine", "rightUp", "horizLine", "leftUp"]],

	"v": [["rightDiag", "", "leftDiag", "rightDiag", "", "leftDiag", "", "", ""]],
	"w": [["vertLine", "vertLine", "vertLine", "vertLine", "vertLine", "vertLine", "horizLine", "horizLine", "horizLine"]],	
	"x": [["rightDiag", "", "leftDiag", "", "", "", "leftDiag", "", "rightDiag"]],
	"y": [["rightDiag", "", "leftDiag", "", "leftDiag", "", "leftUp", "", ""]],
	"z": [["horizLine", "horizLine", "leftDiag", "", "leftDiag", "", "leftDiag", "horizLine", "horizLine"]],

	"t": [["horizLine", "vertLine", "horizLine", "", "vertLine", "", "", "vertLine", ""],
	["", "vertLine", "", "horizLine", "vertLine", "horizLine", "", "vertLine", ""]]
	#"1": [["vertLine", "", "", "vertLine", "", "", "vertLine", "", ""],
	#["", "vertLine", "", "", "vertLine", "", "", "vertLine", ""],
	#["", "", "vertLine", "", "", "vertLine", "", "", "vertLine"]],
	#"0": [["rightDown", "horizLine", "leftDown", "vertLine", "", "vertLine", "rightUp", "horizLine", "leftUp"]]
}










# Separating chars

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


# Creates a new image cut horizontally from original image with given ends
# Name epiphix fron last int given
# String Int Int Int ->
def cutImage(path, xStart, xEnd, i):
	img = Image.open(path)
	img.crop((xStart, 0, xEnd, img.size[1])).save((path[:(len(path) - 4)] + str(i) + ".png"))
	#return img.crop((xStart, 44, xEnd, 0))

# Checks if an image is blank at a given column
# List[List[Int]] Int -> Bool
def columnBlank(array, x):
	column = array[x]
	for y in array[x]:
		if y < 240:
			return False
	return True


# Cuts of white space at top and bottom of image
# String -> 
def vertCropImage(path):
	img = Image.open(path)
	rowArray = arrayByColToRow(imageToArrayByCol(path))

	yStart = 0
	yEnd = len(rowArray)


	if columnBlank(rowArray, 0):
		print("here")
		for i in range(len(rowArray)):
			if columnBlank(rowArray, i) == False:
				if yStart == 0:
					yStart = i
			else:
				yEnd = i
		print(str(yStart) + str(yEnd))
	yStart = max(0, yStart - 2)
	yEnd = min(len(rowArray), yEnd + 2)

	img.crop((0, yStart, img.size[0], yEnd)).save(("CROP" + path))




















