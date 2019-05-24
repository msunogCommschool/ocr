How to use the Optical Character Recognition software:

	1) Open Python and and import * from ocr.py.

	2) Run the function getAllPartitions([image_path]) to create image files 
for the separate characters.
	These image files will be created in the folder with the original image.
	Their filenames will be the original name with an integer afterwards signifying the place of the character in the world (beginning with 0).

	3) Run vertCropImage on each of the single character image files to remove the white space at the top and bottom.
	The resulting files will have the prefix CROP.

	4) Run resizeToStandard([image_path]) on each of the single character image files.
	The resulting files will have the prefix STAN (STANCROP).

	5) If the image is not black and white, run makeBW([image_path]) on each of the single .character image files
	The resulting files will have the prefix BW (BWSTANCROP).

	6) To find the top five potential characters for an image, run topFiveChars([image_path]).
	To find the probability values for all characters for an image, run allCharProbabilities([image_path]).

Notes:
	
	Only works for aphebetical characters
	Currently doesn't support capital letters

For the makeStructDict functions, comment one of the options out.
Use instructions in the code.
By default, the abstracted functions are commented out.