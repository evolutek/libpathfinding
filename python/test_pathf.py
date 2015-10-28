import pathfinding

def main():
	pathf = pathfinding.Pathfinding(30, 20, 1)
	pathf.AddRectangleObstacle(8, 8, 12, 10)
	pathf.AddSquareObstacle(16, 16, 2, "lol")
	pathf.AddCircleObstacle(16, 3, 2)
	pathf.AddRectangleObstacle(12, 12, 19, 12)
	pathf.AddRectangleObstacle(12, 12, 19, 12)
	pathf.RemoveObstaclePosition(12, 12, 19, 12)
	pathf.PrintObstacles()
	pathf.map.ExportMap()
	l = pathf.map.GetNghbrs(15,16)
	for p in l:
		print(str(p))

if __name__ == '__main__':
	main()
