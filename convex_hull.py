import math




from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

	# def getValue(self):
	# 	return self.data

	# def __init__(self, x, y):
	# 	self.x = x
	# 	self.y = y
	# 	self.next = None
	# 	self.prev = None

    # def setNext(self, next_node):
    #     self.next_node = next_node
	#
    # def getNext(self):
    #     return self.next_node
	#
    # def setPrev(self, prev_node):
    #     self.prev = prev_node
	#
    # def getPrev(self):
    #     return self.prev_node
	#
    # def getValue(self):
    #     return self.value



# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
PAUSE = 0.25

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False

# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def showText(self,text):
		self.view.displayStatusText(text)


# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		points.sort(key=lambda point: point.x())
		t2 = time.time()

		node = divideConquer(points)
		currNode = node
		nodeList = []
		while (node.data == currNode.data):
			nodeList.append(currNode)
			currNode = node.next


		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points

		# polygon = [QLineF(points[i],points[(i+1)%3]) for i in range(3)]
		polygon = [QLineF(nodeList[i],nodeList[(i+1)%3]) for i in range(len(nodeList))]

		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

def splitLR(points):
	# Calculate the midpoint index
	mid = len(points) // 2
	# Split the list into 2 halves
	L = points[:mid]
	R = points[mid:]
	return L,R

def divideConquer(points):
		# base case of 1 point: if so return the point as a node
	if (len(points) == 1):
		node = Node(points[0])
		node.next = node
		node.prev = node
		return node
	# base case of 2 points: convert to nodes, connect via
	if (len(points) == 2):
		node1 = Node(points[0])
		node2 = Node(points[1])
		node1.next = node2
		node1.prev = node2
		node2.next = node1
		node2.prev = node1
		return node1, node2
	L,R = splitLR(points)
	left = divideConquer(L)
	right = divideConquer(R)
	return merge(left,right)

def merge(L,R):
	findTangents(L,R)


def findMax(L,R):


def findMin(L,R):


def findTangents(L,R):
	pointList = []

	if not isinstance(L, Node) and (isinstance(L, list) or isinstance(L, tuple)):
		pointMax = L[0]
		currMax = L[0].data.x()
		for curr in L[1:]:
			if curr.data.x() > currMax:
				pointMax = curr
				currMax = curr.data.x
	else:
		pointMax = L
	permL = pointMax
	l = permL

	if not isinstance(R, Node) and (isinstance(R, list) or isinstance(R, tuple)):
		pointMin = R[0]
		currMin = R[0].data.x()
		for curr in R[1:]:
			if curr.data.x() < currMin:
				pointMin = curr
				currMin = curr.data.x
	else:
		pointMin = R
	permR = pointMin
	r = permR

	isLeft = True
	leftDone = False
	rightDone = False
	while not leftDone and not rightDone:
		if (isLeft):
			preslopeL = ((l.data.y()-r.data.y())/(l.data.x()-r.data.x()))
			postslopeL = ((l.prev.data.y()-r.data.y())/(l.prev.data.x()-r.data.x()))
			if (preslopeL > postslopeL):
				l = l.prev
				rightDone = False
			else:
				leftDone = True
		else:
			preslopeR = ((l.data.y()-r.data.y())/(l.data.x()-r.data.x()))
			postslopeR = ((l.data.y()-r.next.data.y())/(l.data.x()-r.next.data.x()))
			if (preslopeR > postslopeR):
				r = r.next
				leftDone = False
			else:
				rightDone = True
		isLeft = not isLeft

	pointList.extend([l,r])

	l = permL
	r = permR

	isLeft = True
	leftDone = False
	rightDone = False
	while not leftDone and not rightDone:
		if (isLeft):
			preslopeL = ((l.data.y()-r.data.y())/(l.data.x()-r.data.x()))
			postslopeL = ((l.next.data.y()-r.data.y())/(l.next.data.x()-r.data.x()))
			if (preslopeL > postslopeL):
				l = l.prev
				rightDone = False
			else:
				leftDone = True
		else:
			preslopeR = ((l.data.y()-r.data.y())/(l.data.x()-r.data.x()))
			postslopeR = ((l.data.y()-r.prev.data.y())/(l.data.x()-r.prev.data.x()))
			if (preslopeR > postslopeR):
				r = r.next
				leftDone = False
			else:
				rightDone = True
		isLeft = not isLeft

	pointList.extend([l,r])

	return pointList


