import cv2
import numpy as np
import copy
import time 


# completed
# Makes the horizontal and vertical lines in immage
def makemineImage(mineImage,blocks,pixelPerBlock):
	(rows,cols) = mineImage.shape
	# print("rows.cols",rows,cols)

	for i in range(1,blocks):
		# vertical lines
		cv2.line(mineImage,(pixelPerBlock*i,0),(pixelPerBlock*i,pixelPerBlock*blocks),white,thickness)
		# horizontal lines
		cv2.line(mineImage,(0,pixelPerBlock*i),(pixelPerBlock*blocks,pixelPerBlock*i),white,thickness)
	
	cv2.imshow("Mine Sweeper",mineImage)
	cv2.waitKey(0)

	return mineImage

# completed
# randomly places mines on the grid
def placeMines(mineMatrix,mineImage,mines,blocks,pixelPerBlock):

	# Shufling indexes to get mine blocks
	randomMines = [x for x in range(0,blocks*blocks)]
	np.random.shuffle(randomMines)
	randomMines = randomMines[:mines]
	mine = 1
	# print(randomMines)

	# Placing mines
	for i in randomMines:
		mineMatrix[i] = mine

	mineMatrix = np.resize(mineMatrix,(blocks,blocks))
	# print("mineMatrix\n",mineMatrix)

	# Showing mines in mine Block
	(rows,cols) = mineMatrix.shape
	for i in range(rows):
		for j in range(cols):
			if mineMatrix[i][j] == mine:
				# print("row {} col {}".format(i,j))
				cv2.rectangle(mineImage,(pixelPerBlock*j,pixelPerBlock*i),(pixelPerBlock*j+pixelPerBlock,pixelPerBlock*i+pixelPerBlock),bomb,fillthickness)

	cv2.imshow("Mine Sweeper",mineImage)
	cv2.waitKey(0)

	return mineMatrix

# Completed
def placeNeighbouringNoofMines(mineMatrix,neighbours,mineImage,blocks,pixelPerBlock):
	(rows,cols) = mineMatrix.shape
	checkNeighbours = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
	mine = 1

	for row in range(rows):
		for col in range(cols):
			for (i,j) in checkNeighbours:
				try:
					# Disabling Negative indexing in python
					# Disable this if, Try with seed(90), you will know
					if row+i <0 or col +j <0:
						continue

					# To not write on the blocks already consisting the bomb
					if mineMatrix[row][col] == mine:
						continue

					# Main Condition
					if mineMatrix[row+i][col+j] == mine:
						neighbours[row][col] = neighbours[row][col] + 1
				except:
					# Letting go of "Index Value exceeded" Error
					pass

	# print("neighbours \n",neighbours)

	# Visualization
	for i in range(rows):
		for j in range(cols):
			if neighbours[i][j] != 0:
				mineImage = cv2.putText(mineImage, str(neighbours[i][j]),(pixelPerBlock*j+spacing,pixelPerBlock*i+spacing+spacing) , font,fontScale, gray, thickness, cv2.LINE_AA)
	cv2.imshow("Mine Sweeper",mineImage)
	cv2.waitKey(0)

	return neighbours


def getLocation(event,x,y,flags,playingMineImage):

	if event == cv2.EVENT_LBUTTONDOWN:
		print("Mouse Clicked at",x,y)
		(x,y) = (int(x/pixelPerBlock),int(y/pixelPerBlock))
		print("Chosen block is",x,y)

		# Cond: If place has bomb
		if mineMatrix[y][x] == mine:
			print("Found a mine")
			cv2.rectangle(playingMineImage,(pixelPerBlock*x,pixelPerBlock*y),(pixelPerBlock*x+pixelPerBlock,pixelPerBlock*y+pixelPerBlock),bomb,fillthickness)
			playingMineImage = cv2.putText(playingMineImage, "#",(pixelPerBlock*x+spacing,pixelPerBlock*y+spacing+spacing) , font,fontScale, black, thickness, cv2.LINE_AA)
			# time.sleep(2)

		# Cond: if the place not empty (for neighbors)
		elif mineMatrix[y][x] == 0 and neighbours[y][x] != 0:
			# cv2.rectangle(mineImage,(pixelPerBlock*x,pixelPerBlock*y),(pixelPerBlock*x+pixelPerBlock,pixelPerBlock*y+pixelPerBlock),white,fillthickness)
			# mineImage = cv2.putText(mineImage, str(neighbours[i][j]),(pixelPerBlock*j+spacing,pixelPerBlock*i+spacing+spacing) , font,fontScale, gray, thickness, cv2.LINE_AA)
			cv2.rectangle(playingMineImage,(pixelPerBlock*x,pixelPerBlock*y),(pixelPerBlock*x+pixelPerBlock,pixelPerBlock*y+pixelPerBlock),white,fillthickness)
			playingMineImage = cv2.putText(playingMineImage, str(neighbours[y][x]),(pixelPerBlock*x+spacing,pixelPerBlock*y+spacing+spacing) , font,fontScale, gray, thickness, cv2.LINE_AA)


		# Cond: if place is empty
		else:
			print("Empty cell")
			cv2.rectangle(playingMineImage,(pixelPerBlock*x,pixelPerBlock*y),(pixelPerBlock*x+pixelPerBlock,pixelPerBlock*y+pixelPerBlock),white,fillthickness)
			pass


	
def mousePointer(playingMineImage):
	cv2.namedWindow("Mine Sweeper")
	cv2.setMouseCallback("Mine Sweeper",getLocation,playingMineImage)
	print("mousePointer\n")

	while True:
		cv2.imshow("Mine Sweeper",playingMineImage)
		if cv2.waitKey(33) == 27:
			break
	# cv2.waitKey(0)



if __name__ == '__main__':

	np.random.seed(90)
	blocks = 9
	mines = 10
	pixelPerBlock = 50
	mine = 1
	mineImage = np.ones((pixelPerBlock*blocks,pixelPerBlock*blocks),dtype=np.uint8)
	mineMatrix = np.zeros((blocks*blocks),dtype=np.int8)
	neighbours  = np.zeros((blocks,blocks),dtype=np.int8)

	# Colors and stuff
	white = [250]
	bomb = [50]
	gray = [150]
	black = [0]
	fillthickness = -1
	thickness = 1
	font = cv2.FONT_HERSHEY_SIMPLEX
	fontScale = 1
	spacing = 20

	# Function Calls
	mineImage = makemineImage(mineImage,blocks,pixelPerBlock)
	playingMineImage = copy.copy(mineImage)
	mineMatrix = placeMines(mineMatrix,mineImage,mines,blocks,pixelPerBlock)
	neighbours = placeNeighbouringNoofMines(mineMatrix,neighbours,mineImage,blocks,pixelPerBlock)
	mousePointer(playingMineImage)

	# openingAlgorithm()
	print("mineMatrix\n",mineMatrix)
	print("neighbours\n",neighbours)

	# cv2.imshow("Mine Sweepers",playingMineImage)
	# cv2.waitKey(10)

	events = [i for i in dir(cv2) if 'EVENT' in i]
	# print( events )

	cv2.destroyAllWindows()

