import pathfinding
import interface
import timeit
import functools
from random import randint

def main():

	pathf = pathfinding.Pathfinding(3000, 2000, 150)
	'''
	while path == None:
		x1 = randint(1,3000)
		x2 = randint(1,3000)
		y1 = randint(1,2000)
		y2 = randint(1,2000)
		a = pathfinding.Point(x1, y1)
		b = pathfinding.Point(x2, y2)
		print("(" + str(a) + "," + str(b) + ")")
		path = pathf.ComputePath(a, b, 10)
	print(str(path))
	'''
	
	# Present obstacle on the table
	pathf.AddRectangleObstacle(0, 1750, 250, 2000)
	pathf.AddRectangleObstacle(2750, 1750, 3000, 2000)
	pathf.AddRectangleObstacle(2700, 595, 3000, 1100)
	pathf.AddRectangleObstacle(794, 0, 832, 200)
	pathf.AddRectangleObstacle(2172, 0, 2210, 200)
	pathf.AddRectangleObstacle(895, 740, 1476, 777)
	pathf.AddRectangleObstacle(1527, 740, 2106, 777)
	pathf.AddRectangleObstacle(1476, 740, 1527, 1355)
	
	path = pathf.ComputePath(pathfinding.Point(500, 1300), pathfinding.Point(2500, 1300))
	pathf.ExportAll(path)

	inter = interface.Interface()
	inter.update()
	#print(timeit.timeit(functools.partial(pathf.ComputePath, pathfinding.Point(40, 120), pathfinding.Point(2003, 1204), 10), number = 1000))

if __name__ == '__main__':
	main()
