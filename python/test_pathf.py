import pathfinding
import timeit
import functools

def main():
	pathf = pathfinding.Pathfinding(3000, 2000, 15)
	pathf.AddRectangleObstacle(80, 80, 120, 100)
	pathf.AddSquareObstacle(160, 160, 20, "lol")
	pathf.AddCircleObstacle(160, 30, 20)
	pathf.AddRectangleObstacle(120, 120, 190, 120)
	pathf.AddRectangleObstacle(120, 120, 190, 120)
	pathf.RemoveObstaclePosition(120, 120, 190, 120)
	pathf.PrintObstacles()
	print(timeit.timeit(functools.partial(pathf.ComputePath, pathfinding.Point(40, 120), pathfinding.Point(2003, 1204), 10), number = 1000))

if __name__ == '__main__':
	main()
