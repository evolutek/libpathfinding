#!/usr/bin/env python3

# Example :
# import pathfinding
# pathf = Pathfinding(3000, 2000, 100)
# pathf.AddRectangleObstacle(200, 200, 100, 100)
# pathf.map.ExportMap()

from math import sqrt
import sys

# Class to create point:
# all point have a cost (Empty, Obstacle, Border)
class Point:

	def __init__(self, x, y, cost = None):
		self.x = x
		self.y = y
		self.cost = cost

	# Permite to convert a point to string
	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

# Class to create obstacle :
# (x, y) is the center
# (x1, y1) and (x2, y2) is the two corner
class Obstacle:

	def __init__(self, x1, y1, x2, y2, tag):
		self.x = round((x1 + x2)/2)
		self.y = round((y1 + y2)/2)
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.tag = tag

	# Permite to convert an obstacle to string
	def __str__(self):
		return self.tag + " (" + str(self.x1) + ", " + str(self.y1) + "), (" + str(self.x2) + ", " + str(self.y2) + ")"

# Class to create a path with his starting point
class Path:

	def __init__(self, p):
		self.listofpoint = []
		self.start = p
		self.listofpoint.append(p)

	# Can add a point to the path
	def AddPoint(self, p):
		self.listofpoint.append(p)

	# Can remove a point to the path
	def RemovePoint(self, point):
		for p in self.listofpoint:
			if p == point:
				self.listofpoint.remove(p)
				return "Done"
		return "Error not found"

	# Compute the cost of the path
	def ComputeCost(self):
		cost = 0
		for i in range(0, len(path)-1):
			cost =+ (sqrt((path[i].x - path[i+1].x)**2 + (path[i].y - path[i+1].y)**2))
		return cost

	# Return the number of point in a path
	def __len__(self):
		return len(self.listofpoint)
	
	def __str__(self):
		s = ""
		for p in self.listofpoint:

			s += str(p) + " -> "
		return s

	# Debug part

	# Print the path on the map
	def PrintPath(self):
		for p in self.listofpoint:
			print(str(p))


# Class to create the map:
# w and h are the width and the hight
# Can set and remove obstacle in the map
class Map:

	def __init__(self, w, h, robot_radius, obstaclecost, emptycost, bordercost):
		self.w = w
		self.h = h
		self.ObstacleCost = obstaclecost
		self.EmptyCost = emptycost
		self.BorderCost = bordercost
		self.map = []
		for x in range(0, self.h+1):
			self.map.append([])
			for y in range(0, self.w+1):
				if(x == 0 or x == h or y == 0 or y == w):
					self.map[x].append(Point(y, x, self.BorderCost))
				else:
					self.map[x].append(Point(y, x, self.EmptyCost))
		self.robot_radius = robot_radius

	# Set the cost of a cell to obstacle
	def SetObstacle(self, y, x):
		# print("set obstacle at point (" + str(x + 1) + ", " + str(y + 1) + ")")
		self.map[x][y].cost += self.ObstacleCost
	
	# Set the cost of a cell to empty
	def RemoveObstacle(self, y, x):
		self.map[x][y].cost -= self.ObstacleCost
	
	# Return a point of the map
	def GetPoint(self, y, x):
		return self.map[x][y]

	# Return a point if it is in the map else return None
	def GetPointFromMap(self, x, y):
		valid = (x >= self.robot_radius
			and x <= self.h - self.robot_radius
			and y >= self.robot_radius
			and y <= self.w - self.robot_radius)
		return self.map[y][x] if valid else None

	# Return a list of the neighborhoods of a point of the map
	def GetNghbrs(self, y, x):
		N = []
		N.append(self.GetPointFromMap(x - 1, y))
		N.append(self.GetPointFromMap(x + 1, y))
		N.append(self.GetPointFromMap(x, y - 1))
		N.append(self.GetPointFromMap(x, y + 1))
		N.append(self.GetPointFromMap(x - 1, y - 1)) 
		N.append(self.GetPointFromMap(x - 1, y + 1))
		N.append(self.GetPointFromMap(x + 1, y - 1))
		N.append(self.GetPointFromMap(x + 1, y + 1))
		return [x for x in N if x is not None]
	
	# Return if the robot can access to a point
	def IsBlocked(self, y, x):
		if(x <= self.robot_radius or
			x >= (self.h - self.robot_radius) or
			y <= self.robot_radius or
			y >= self.w - self.robot_radius):
			return True
		return self.map[x][y].cost != self.EmptyCost

    # Debug Part

	# Print all the map
	def PrintMap(self):
		for x in range(self.h+1):
			s = ""
			for y in range(self.w+1):
				if self.map[x][y].cost == self.EmptyCost:
					s += ' '
				elif self.map[x][y].cost == self.BorderCost:
					s += '#'
				else:
					s += 'X'
			print(s)

	# Create a .txt of the map
	def ExportMap(self):
		fimap = open('map.txt', 'w')
		print("file create")
		for x in range(0,self.h+1):
			for y in range(0,self.w+1):
				if self.map[x][y].cost == self.EmptyCost:
					fimap.write(' ')
				elif self.map[x][y].cost == self.BorderCost:
					fimap.write('#')
				else:
					fimap.write('X')
			fimap.write('\n')
		fimap.close()

# Class to call to create an object pathfinding with a map with :
# The map weidth
# The map height
# The robot radius
class Pathfinding:

	def __init__(self, mapw, maph, _robot_radius):
		self.obstacles = []
		self.ObstacleCost = 10000
		self.EmptyCost = 0
		self.BorderCost = 99999
		self.robot_radius = _robot_radius
		self.map = Map(mapw, maph, self.robot_radius, self.ObstacleCost, self.EmptyCost, self.BorderCost)

	# Compute the distance between two position
	def DistancePositionToPosition(self, x1, y1, x2, y2):
		return sqrt((x1 - x2)**2 + (y1 - y2)**2)

	# Compute the distance between two point
	def DistancePointToPoint(self, p1, p2):
		return self.DistancePositionToPosition(p1.x, p1.y, p2.x, p2.y)

	# Add a rectangular obstacle
	def AddRectangleObstacle(self, x1, y1, x2, y2, tag = "no tag"):
		self.obstacles.append(Obstacle(x1, y1, x2, y2, tag))
		for i in range(x1-1, x2):
			for j in range(y1-1, y2):
				self.map.SetObstacle(i, j)

	# Add a square obstacle
	def AddSquareObstacle(self, x, y, radius, tag = "no tag"):
		self.AddRectangleObstacle(x - (radius - 1), y - (radius - 1), x + (radius - 1), y + (radius - 1), tag)

	# Add a circle obstacle
	def AddCircleObstacle(self, x, y, radius, tag = "not tag"):
		self.AddSquareObstacle(x, y, radius, tag)

	# Remove an obstacle
	def RemoveObstacle(self, obstacle):
		for i in range(obstacle.x1-1, obstacle.x2):
			for j in range(obstacle.y1-1, obstacle.y2):
				self.map.RemoveObstacle(i, j)

	# Rmove an obstacle with the tag
	def RemoveObstacleTag(self, tag):
		for obstacle in self.obstacles:
			if obstacle.tag == tag: 
				self.RemoveObstacle(obstacle)
				self.obstacles.remove(obstacle)

	# Remove an obstacle with the position
	def RemoveObstaclePosition(self, x, y, a = -1, b = -1):
		if a == -1 and b == -1:
			for obstacle in self.obstacles:
				if obstacle.x == x and obstacle.y == y:
					self.RemoveObstacle(obstacle)
					self.obstacles.remove(obstacle)
		else:
			for obstacle in self.obstacles:
				if obstacle.x1 == x and obstacle.y1 == y and obstacle.x2 == a and obstacle.y2 == b:
					self.RemoveObstacle(obstacle)
					self.obstacles.remove(obstacle)

	# Remove all the obstacles of the list of obstacles
	def ClearObstacles(self):
		self.obstacles.clear()

	def ComputeLineOfSight(self, p1, p2):
		coef = (p2.y - p1.y) / (p2.x - p1.x)
		ordo = p1.y - (coef * p1.x)
		line = []
		for x in range(min(p1.x, p2.x)+1, max(p1.x, p2.x)):
			line.append(Point(x, int(x * coef + ordo)))
		return line

	# Test if there is nos obstacle on the line of sight between two point
	def IfOnLineOfSight(self, p1, p2):
		line = self.ComputeLineOfSight(p1, p2)
		for p in line:
			if self.map.IsBlocked(p.x, p.y):
				print("There is an obstacle in : " + str(p))
				return True
		print("No obstacle")
		return False

	# Return the point of collision with the first obstacle in the line of Sight and the obstacle
	def ComputeListOfCollision(self, p1, p2):
		line = self.ComputeLineOfSight(p1, p2)
		collision = []
		for p in line:
			if self.map.IsBlocked(p.x, p.y):		
				print("There is an obstacle in : " + str(p))
				for obstacle in self.obstacles:
					if p.x >= obstacle.x1 and p.x <= obstacle.x2 and p.y >= obstacle.y1 and p.y <= obstacle.y2:
						print(str(obstacle))
						if collision == [] or obstacle != (collision[len(collision) - 1])[1]:
							collision.append((p, obstacle))
		print("List of collision finish")
		return collision

	# Return the side of an obstacle

	#              b1
	#          -----------
	#          |         |
	#      a1  |         |  a2
	#          |         |
	#          -----------
	#              b2

	# a1 and b1 : right
	# a2 and b2 : left

	# 1 : a
	# 2 : b

	def SelectSide(self, obstacle, p):
		if p.x == obstacle.x1 or p.x == obstacle.x2:
			return 1
		else:
			return 2
	
	# Return a point to pass by the rigth of an obstacle
	def ComputeFromRight(self, collision):
		p = collision[0]
		obstacle = collision[1]
		side = self.SelectSide(obstacle, p)
		if side == 2:
			pointofliberty = Point((obstacle.x1 - self.robot_radius - int((sqrt(3)/2) * (obstacle.y2 - obstacle.y1)//2)), ((obstacle.y2 - obstacle.y1)//2 + obstacle.y1))
		else:
			pointofliberty = Point(((obstacle.x2 - obstacle.x1)//2 + obstacle.x1), (obstacle.y2 + self.robot_radius + int((sqrt(3)/2) * (obstacle.x2 - obstacle.x1)//2)))
		if self.map.IsBlocked(pointofliberty.x, pointofliberty.y):
			print("Error in computing p r")
			return None
		else:
			return pointofliberty

	# Compute a path from the left of an obstacle
	def ComputeFromLeft(self, collision):
		p = collision[0]
		obstacle = collision[1]
		side = self.SelectSide(obstacle, p)
		if side == 2:
			pointofliberty = Point((obstacle.x2 + self.robot_radius + int((sqrt(3)/2) * (obstacle.y2 - obstacle.y1)//2)), (obstacle.y1 + (obstacle.y2 - obstacle.y1)//2))
		else:
			pointofliberty = Point((obstacle.x1 + (obstacle.x2 - obstacle.x1)//2), (obstacle.y1 - self.robot_radius - int((sqrt(3)/2) * (obstacle.x2 - obstacle.x1)//2)))
		if self.map.IsBlocked(pointofliberty.x, pointofliberty.y):
			print("Error in computing p l")
			return None
		else:
			return pointofliberty

	# Return if a path is possible
	def IsPossible(self, path):
		for i in range(0, len(path)-1):
			if self.IfOnLineOfSight(path.listofpoint[i], path.listofpoint[i+1]):
				print("Path not possible")
				return False
		return True

	# Compute the better path between two point with stop as the number of iteration before stop
	def ComputePath(self, p1, p2, stop = 10):
		if self.map.IsBlocked(p1.x, p1.y) or self.map.IsBlocked(p2.x, p2.y):
			print("Incorrect Point")
			return None
		allpath = []
		path = Path(p1)
		path.AddPoint(p2)
		allpath.append(path)
		for n in range (stop + 1):
			found = None
			for path in allpath:
				if self.IsPossible(path) and (found == None or (path.ComputeCost() < found.ComputeCost())):
					print("A path is possible")
					found = path
			if found != None:
				print("Path found after " + str(n) + " iterations")
				print("Path is : " + str(path))
				return found
			else:
				_allpath = []
				for path in allpath:
					pathr = Path(p1)
					pathl = Path(p1)
					failr = False
					faill = False
					for i in range(1, len(path)):
						print("i : " + str(i))
						print("Analyse path between " + str(path.listofpoint[i-1]) + " and " + str(path.listofpoint[i]))
						if self.IfOnLineOfSight(path.listofpoint[i-1], path.listofpoint[i]):
							collision = self.ComputeListOfCollision(path.listofpoint[i-1], path.listofpoint[i])
							for col in collision:
								print("analyse collision")
								if not failr:
									print("Compute from right")
									pointr = (self.ComputeFromRight(col))
									if pointr == None:
										failr = True
									else:
										pathr.AddPoint(pointr)
								if not faill:
									print("Compute from left")
									pointl = (self.ComputeFromLeft(col))
									if pointl == None:
										faill = True
									else:
										pathl.AddPoint(pointl)
							pathr.AddPoint(path.listofpoint[i])
							pathl.AddPoint(path.listofpoint[i])
					allpath.remove(path)
					if not failr:
						_allpath.append(pathr)
					if not faill:
						_allpath.append(pathl)
				if _allpath == []:
					print("Can't find a path")
					return None
				allpath = _allpath
		print("No path found before doing " + str(stop) + " iterations")
		return None

	# Debug Part

	# Print all the obstacles
	def PrintObstacles(self):
		for obstacle in self.obstacles:
			print(str(obstacle))
