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
		return (self.tag + " (" + str(self.x1) + ", " + str(self.y1) 
		+ "), (" + str(self.x2) + ", " + str(self.y2) + ")")

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
		for i in range(len(self.listofpoint)):
			s += str(self.listofpoint[i])
			if i != (len(self.listofpoint) - 1):
				s += " -> "
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

	def __init__(self, w, h, robot_radius, obstaclecost, emptycost):
		self.w = w
		self.h = h
		self.ObstacleCost = obstaclecost
		self.EmptyCost = emptycost
		self.map = []
		for x in range(self.h):
			self.map.append([])
			for y in range(self.w):
				self.map[x].append(Point(y, x, self.EmptyCost))
		self.map = self.InvMatrix(self.map)
		self.robot_radius = robot_radius
	
	def InvMatrix(self, matrix):
		m = []
		for i in range(self.w):
			m.append([])
			for j in range(self.h):
				m[i].append(matrix[j][i])
		return m

	# Set the cost of a cell to obstacle
	def SetObstacle(self, x, y):
		# print("set obstacle at point (" + str(x + 1) + ", " + str(y + 1) + ")")
		self.map[x][y].cost += self.ObstacleCost
	
	# Set the cost of a cell to empty
	def RemoveObstacle(self, x, y):
		self.map[x][y].cost -= self.ObstacleCost
	
	# Return a point of the map
	def GetPoint(self, x, y):
		return self.map[x][y]

	# Return if it is in the map
	def IsFromMap(self, x, y):
		return (x >= self.robot_radius
			and x <= self.w - self.robot_radius
			and y >= self.robot_radius
			and y <= self.h - self.robot_radius)

	# Return if the robot can access to a point
	def IsBlocked(self, x, y):
		x1 = x - self.robot_radius
		x2 = x + self.robot_radius
		y1 = y - self.robot_radius
		y2 = y + self.robot_radius
		if(x1 >= 0 and x2 <= self.w
			and y1 >= 0 and y2 <= self.h):
			for a in range(x1, x2 + 1):
				for b in range(y1, y2 + 1):
					if self.map[a][b].cost != self.EmptyCost:
						print("Obstacle detected")
						return True
			return False
		else:
			print("Point not in the map")
			return True

	# Debug Part

	# Create a .txt of the map
	def ExportMap(self):
		fimap = open('map', 'w')
		print("file create")
		for x in range(0,self.w):
			for y in range(0,self.h):
				if self.map[x][y].cost == self.EmptyCost:
					fimap.write(' ')
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
		self.robot_radius = _robot_radius
		self.map = Map(mapw, maph, self.robot_radius, self.ObstacleCost,
						self.EmptyCost)

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
		self.AddRectangleObstacle(x - (radius - 1), y - (radius - 1), x
		+ (radius - 1), y + (radius - 1), tag)

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
				if (obstacle.x1 == x and obstacle.y1 == y and obstacle.x2 == a
					and obstacle.y2 == b):
					self.RemoveObstacle(obstacle)
					self.obstacles.remove(obstacle)

	# Remove all the obstacles of the list of obstacles
	def ClearObstacles(self):
		self.obstacles.clear()

	def ComputeLineOfSight(self, p1, p2):
		r = 0
		if p1.x == p2.x:
			r = 1
		coef = (p2.y - p1.y) / (p2.x - p1.x + r)
		ordo = p1.y - (coef * p1.x)
		line = []
		for x in range(min(p1.x, p2.x)+1, max(p1.x, p2.x),5):
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

	# Return the point of collision with the first obstacle in the line of sight and the obstacle
	def ComputeFirstCollision(self, p1, p2):
		line = self.ComputeLineOfSight(p1, p2)
		for p in line:
			if self.map.IsBlocked(p.x, p.y):		
				print("There is an obstacle in : " + str(p))
				return self.SearchCollision(p)
		print("No obstacle detected")
		return None
	

	# Point of the robot

	#     c1
	#
	#    0|1
	# p1
	#	x---x  0
	#   | R |  - c2
	#   x---x  1
	#        p2

	# Return the obstacle in a range between the point given and the collision point 
	def SearchCollision(self, p):
		p1 = Point(p.x - self.robot_radius, p.y - self.robot_radius)
		p2 = Point(p.x + self.robot_radius, p.y + self.robot_radius)
		possible = []
		for obstacle in self.obstacles:
			for x in range(p1.x, p2.x+1):
				if x >= obstacle.x1 and x <= obstacle.x2:
					possible.append((obstacle, x, 0))
		for obstacle in possible:
			for y in range(p1.y, p2.y+1):
				if y < obstacle[0].y1 or y > obstacle[0].y2:
					possible.remove(obstacle)
					break
				else:
					obstacle[2] = y
		collision = possible[0]
		if collision[1] < ((p1.x + p2.x)/2):
			x = p1.x 
		else:
			x = p2.x
		if collision[2] < ((p1.y + p2.y)/2):
			y = p1.y
		else:
			y = p2.y
		difxc = abs(x - collision[1])
		difyc = abs(y - collision[2])
		for obstacle in possible:
			difx = abs(x - obstacle[1])
			dify = abs(y - obstacle[2])
			if difx < difxc and dify < difyc:
				collision = obstacle
				difxc = difx
				difyc = dify
		collision = [Point(collision[1], collision[2]), collision[0]]
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
			d = ((obstacle.y2 - obstacle.y1) // 2)
			x = (obstacle.x1 - (2 * self.robot_radius) - int((sqrt(3)/2) * d))
			y = (d + obstacle.y1)
		else:
			d = ((obstacle.x2 - obstacle.x1) // 2)
			x = (d + obstacle.x1)
			y = (obstacle.y2 + (2 * self.robot_radius) + int((sqrt(3)/2) * d))
		if self.map.IsFromMap(x, y):
			return Point(x, y)
		else:
			return None

	# Compute a path from the left of an obstacle
	def ComputeFromLeft(self, collision):
		p = collision[0]
		obstacle = collision[1]
		side = self.SelectSide(obstacle, p)
		if side == 2:
			d = ((obstacle.y2 - obstacle.y1) // 2)
			x = (obstacle.x2 + (2 * self.robot_radius) + int((sqrt(3)/2) * d))
			y = (d + obstacle.y1)
		else:
			d = ((obstacle.x2 - obstacle.x1) // 2)
			x = (d + obstacle.x1)
			y = (obstacle.y1 - (2 * self.robot_radius) - int((sqrt(3)/2) * d))
		if self.map.IsFromMap(x, y):
			return Point(x, y)
		else:
			return None

	# Return if a path is possible
	def IsPossible(self, path):
		for i in range(0, len(path)-1):
			if self.IfOnLineOfSight(path.listofpoint[i], path.listofpoint[i+1]):
				print("Path not possible")
				return False
		print("Path possible")
		return True

	# Init the computation of the path
	def InitComputePath(self, p1, p2):
		if self.map.IsBlocked(p1.x, p1.y):
			print("Incorrect Starting Point")
			return False
		if self.map.IsBlocked(p2.x, p2.y):
			print("Incorrect Ending Point")
			return False
		print("Starting Computing Path between : " + str(p1) + " and " + str(p2))
		return True

	# Search if there is a path is correct
	def SearchForACorrectPath(self, listofpath):
		found = None
		for path in listofpath:
			if (self.IsPossible(path) and 
				(found == None or path.ComputeCost() < found.ComputeCost())):
				print("Correct path found")
				found = path
		if found != None:
			print("Path found : " + str(path))
		return found

	# Compute two path to pass the first obstacle
	def ComputeTwoPath(self, path):
		pathr = Path(path.start)
		pathl = Path(path.start)
		listofpath = []
		failr = False
		faill = False
		for i in range(1, len(path)):
			computed = False
			pa = path.listofpoint[i-1]
			pb = path.listofpoint[i]
			coll = self.ComputeFirstCollision(pa, pb)
			if coll != None and not computed:
				computed = True
				if not failr:
					print("Compute from right")
					pr = self.ComputeFromRight(coll)
					if pr == None:
						failr = True
					else :
						pathr.AddPoint(pr)
						pathr.AddPoint(pb)
						listofpath.append(pathr)
				if not faill:
					print("Compute from left")
					pl = self.ComputeFromLeft(coll)
					if pl == None:
						faill = True
					else:
						pathl.AddPoint(pl)
						pathl.AddPoint(pb)
						listofpath.append(pathl)
		return listofpath
			

	# Compute the better path between two point with stop as the number of iteration before stop
	def ComputePath(self, p1, p2, stop = 10):
		if not self.InitComputePath(p1, p2):
			return None
		allpath = []
		path = Path(p1)
		path.AddPoint(p2)
		allpath.append(path)
		for n in range (1, stop + 1):
			print("Search for a correct path")
			searched = self.SearchForACorrectPath(allpath)
			if searched != None:
				return searched
			_allpath = []
			for path in allpath:
				print("Compute two path")
				lp = self.ComputeTwoPath(path)
				allpath.remove(path)
				for path in lp:
					_allpath.append(lp)
			if _allpath == []:
				print("Can't find a path")
				return None
			allapth = _allpath
		print("No path found before doing " + str(stop) + " iterations")
		return None

	# Debug Part

	# Print all the obstacles
	def PrintObstacles(self):
		for obstacle in self.obstacles:
			print(str(obstacle))

	# Export all the data off the map
	def ExportAll(self, path = []):
		fi = open('all', 'w')
		print("file create")
		fi.write('obstacles\n')
		for obstacle in self.obstacles:
			fi.write(str(obstacle.x1)+'\n')
			fi.write(str(obstacle.x2)+'\n')
			fi.write(str(obstacle.y1)+'\n')
			fi.write(str(obstacle.y2)+'\n')
		fi.write('path\n')
		if path != []:
			for p in path.listofpoint:
				fi.write(str(p)+'\n')
		fi.write('robot\n')
		fi.write(str(self.robot_radius)+'\n')
		fi.close()

