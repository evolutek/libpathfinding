from tkinter import *

class Interface:
	
	def __init__(self):
		self.window = Tk()
		self.button = Button(self.window, text="Close", command=self.window.quit)
		self.button.pack()
		self.canvas = Canvas(self.window, width=1500, height=1000, background='black')
		self.mapimage = PhotoImage(file="map.png")
		self.canvas.create_image(750, 500, image=self.mapimage)
		self.canvas.pack()
		print("Window created")
		self.window.after(1000, self.update)
		self.window.mainloop()

	def update(self):
		print("Window updating")
		print("Updating Data")
		filemap = open('all')
		print("Delete Old Data")
		self.canvas.delete("all")
		self.canvas.create_image(750, 500, image=self.mapimage)
		fmap = filemap.readlines()
		filemap.close()
		i = 1
		while fmap[i] != 'path\n' or i >= len(fmap):
			print("Add Obstacle")
			o = self.read_obstacle(fmap, i)
			self.canvas.create_rectangle(o[0], o[2], o[1], o[3], fill="red")
			i += 4
		i += 1
		path = []
		while fmap[i] != 'robot\n':
			path.append(fmap[i])
			i += 1
		radius = int(fmap[i+1])//2
		for i in range(len(path)):
			path[i] = self.read_point(path[i])
		print("Add Path")
		for i in range(1, len(path)):
			line = self.ComputeLOS(path[i-1], path[i])
			for i in range(len(line)):
				x1 = line[i][0] - radius
				x2 = line[i][0] + radius
				y1 = line[i][1] - radius
				y2 = line[i][1] + radius
				color = "blue"
				if i == 0 or i == (len(line) - 1):
					color = "green"
				self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
		for i in range(1, len(path)):
			self.canvas.create_line(path[i-1][0], path[i-1][1], path[i][0],
										path[i][1], fill="magenta", width=15)
		self.window.after(1000, self.update)

	def read_obstacle(self, obstacle, i):
		x1 = int(obstacle[i])//2
		x2 = int(obstacle[i+1])//2
		y1 = int(obstacle[i+2])//2
		y2 = int(obstacle[i+3])//2
		return (x1, x2, y1, y2)

	def read_point(self, s):
		s1 = ''
		i = 1
		while s[i] != ',':
			s1 += s[i]
			i += 1
		s2 =''
		i += 2
		while s[i] != ')':
			s2 += s[i]
			i += 1
		return (int(s1)//2, int(s2)//2)
	
	def ComputeLOS(self, p1, p2):
		r = 0
		if p1[0] == p2[0]:
			r = 1
		coef = (p2[1] - p1[1]) / (p2[0] - p1[0] + r)
		ordo = p1[1] - (coef * p1[0])
		line = []
		for x in range(min(p1[0], p2[0])+1, max(p1[0], p2[0]), 25):
			line.append((x, int(x * coef + ordo)))
		return line
