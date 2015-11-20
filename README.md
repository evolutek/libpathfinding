# libpathfinding

This is a library to generate a map, add/remove obstacle on it
and compute a path between to point by seeing the map.

How to use it in Python 3.5
---------------------------

import pathfinding

pf = pathfinding.Pathfinding(3000, 2000, 20)  
pf.AddRctangleObstacle(80, 80, 120, 100)  
pf.AddSquareObstacle(1250, 900, 20, "Robot")  
pf.RemoveObstaclePosition(80, 80, 120, 100)  

path = pf.ComputePath(pathfinding.Point(40, 120), pathfinding.Point(2000, 1200), 10)

###Library in Python 3.5 by Corentin 'Kmikaz' Vigourt
