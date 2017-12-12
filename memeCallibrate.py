from pylsl import StreamInlet, resolve_stream
from numpy import mean
def calibrate(inlet):
	#220 hz
	
	left = []
	right = []
	up = []
	down = []
	#blink was x,w
	#[x,y,z,w]
	#left is y or z
	#right is y or z
	#up is w or x
	#down is w or x	
	

	print "look left"
	while len(left) < 220:
		left.append(inlet.pull_sample()[0][1])
	mLeft = (.8*(max(left)-mean(left)))+mean(left)
	
	print "look right"
	while len(right) < 220:
		right.append(inlet.pull_sample()[0][2])
	mRight = (.8*(max(right)-mean(right)))+mean(right)

	print "look up"
	while len(up) < 220:
		up.append(inlet.pull_sample()[0][0])
	mUp = (.8*(min(up)-mean(up)))+mean(up)

	print "look down"
	while len(down) < 220:
		down.append(inlet.pull_sample()[0][3])
	mDown = (.8*(max(down)-mean(down)))+mean(down)
	
  	return [mUp,mLeft,mRight,mDown]