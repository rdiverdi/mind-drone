def calibrate(inputs):
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
		left.append(inputs[1])
	mLeft = .8*max(left)
	
	print "look right"
	while len(right) < 220:
		left.append(inputs[2])
	mRight = 1.2*min(right)

	print "look up"
	while len(up) < 220:
		left.append(inputs[0])
	mUp = .8*max(up)

	print "look down"
	while len(down) < 220:
		left.append(inputs[3])
	mDown = 1.2*min(down)
	
  return [mLeft,mRight,mUp,mDown]
	 
