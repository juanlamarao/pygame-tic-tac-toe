import pygame

# Screen settings
FPS = 60
WIDTH = 600
HEIGHT = 600
lineWidth = 2
lineColor = "black"
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()

# classes
class Table():
	def __init__(self):
		self.table = [
			["", "", ""],
			["", "", ""],
			["", "", ""]
		]
		self.turn = 'x'
		self.complete = False
		self.winner = ''
		self.movesCount = 0
		self.lastmove = ()

	def mouse_position_table(self):
		col = int(mouse[0]/(WIDTH/3))
		row = int(mouse[1]/(HEIGHT/3))
		return col, row

	def hovered_square_content(self):
		col, row = self.mouse_position_table()
		return self.table[row][col]

	def hovered_square_center(self):
		col, row = self.mouse_position_table()
		x = (col*100)+((col+1)*100)
		y = (row*100)+((row+1)*100)
		return x, y

	def print_measures(self):
		measures = self.hovered_square_measures()
		print(f"xStart: {measures['xStart']}, yStart: {measures['yStart']}, xCenter: {measures['xCenter']}, yCenter: {measures['yCenter']}, xEnd: {measures['xEnd']}, yEnd: {measures['yEnd']}")

	def hovered_square_measures(self):
		x, y = self.mouse_position_table()
		xLineOffset = lineWidth if x else 0
		yLineOffset = lineWidth if y else 0
		xThird = WIDTH / 3
		yThird = HEIGHT / 3
		xStart = (x * xThird) + xLineOffset
		yStart = (y * yThird) + yLineOffset
		xCenter = xStart + ((xThird / 2) - xLineOffset)
		yCenter = yStart + ((yThird / 2) - yLineOffset)
		xEnd = xCenter + (xThird / 2)
		yEnd = yCenter + (yThird / 2)

		return {
			'x': x,
			'y': y,
			'xStart': int(xStart),
			'yStart': int(yStart),
			'xCenter': int(xCenter),
			'yCenter': int(yCenter),
			'xEnd': int(xEnd),
			'yEnd': int(yEnd)
		}

	def empty_square(self):
		col, row = self.mouse_position_table()
		return not self.table[row][col]

	def table_full(self):
		return self.movesCount == 9

	def someone_won(self):
		xOffset = (((WIDTH/3)/2)/2)+10
		yOffset = (((WIDTH/3)/2)/2)+10
		x = ((WIDTH/3)/2)
		y = ((HEIGHT/3)/2)
		valid = [
			# diagonais
			(table.table[0][0] and table.table[0][0] == table.table[1][1] and table.table[1][1] == table.table[2][2], (x-xOffset, y-yOffset, (x*5)+xOffset, (y*5)+yOffset)),
			(table.table[0][2] and table.table[0][2] == table.table[1][1] and table.table[1][1] == table.table[2][0], ((x*5)+xOffset, y-yOffset, x-xOffset, (y*5)+yOffset)),
			# linhas
			(table.table[0][0] and table.table[0][0] == table.table[0][1] and table.table[0][1] == table.table[0][2], (x-xOffset, y, (x*5)+xOffset, y)),
			(table.table[1][0] and table.table[1][0] == table.table[1][1] and table.table[1][1] == table.table[1][2], (x-xOffset, y*3, (x*5)+xOffset, y*3)),
			(table.table[2][0] and table.table[2][0] == table.table[2][1] and table.table[2][1] == table.table[2][2], (x-xOffset, y*5, (x*5)+xOffset, y*5)),
			# colunas 
			(table.table[0][0] and table.table[0][0] == table.table[1][0] and table.table[1][0] == table.table[2][0], (x, y-yOffset, x, (y*5)+yOffset)),
			(table.table[0][1] and table.table[0][1] == table.table[1][1] and table.table[1][1] == table.table[2][1], (x*3, y-yOffset, x*3, (y*5)+yOffset)),
			(table.table[0][2] and table.table[0][2] == table.table[1][2] and table.table[1][2] == table.table[2][2], (x*5, y-yOffset, x*5, (y*5)+yOffset))
		]
		for entry in valid:
			if entry[0]:
				return entry[1]
		
		return False

	def input_turn(self):
		col, row = self.mouse_position_table()
		self.table[row][col] = self.turn
		self.movesCount += 1
		self.lastmove = col, row
		if self.movesCount > 3:
			self.update_winner()

	def update_winner(self):
		coord = self.someone_won()
		if coord:
			self.winner = self.turn
			self.winnerSquares = coord
			pygame.time.wait(500)
			pygame.draw.line(screen, "green", (coord[0], coord[1]), (coord[2], coord[3]), 5)
			pygame.display.flip()
			pygame.time.wait(2000)
		elif self.table_full():
			self.winner = 'd'
			pygame.time.wait(2000)
		else:
			pass

	def change_turn(self):
		self.turn = "o" if self.turn == "x" else "x"

	def play(self):
		if pygame.mouse.get_focused():
			if self.empty_square():
				self.input_turn()
				self.change_turn()

	def render_hover(self):
		if pygame.mouse.get_focused():
			measures = self.hovered_square_measures()
			if not self.table[measures['y']][measures['x']]:
				rect = pygame.Rect(measures['xStart'], measures['yStart'], measures['xEnd']-measures['xStart'], measures['yEnd']-measures['yStart'])
				pygame.draw.rect(screen, "red", rect)
				# pygame.draw.circle(screen, "green", (measures['xCenter'], measures['yCenter']), 3, 3)
				exec(f"draw_{self.turn}({measures['xCenter']}, {measures['yCenter']})")

	def render_moves(self):
		for r, row in enumerate(self.table):
			for c, col in enumerate(row):
				if col:
					centerX = (c*(WIDTH/3))+(WIDTH/6)
					centerY = (r*(HEIGHT/3))+(HEIGHT/6)
					exec(f'draw_{col}({centerX}, {centerY})')

# control
run = True
table = Table()

# aux functions
def draw_background():
	for i in range(1, 3):
		pygame.draw.line(screen, lineColor, (int((WIDTH/3)*i),0), (int((WIDTH/3)*i),HEIGHT), lineWidth)
		pygame.draw.line(screen, lineColor, (0,int((HEIGHT/3)*i)), (WIDTH,int((HEIGHT/3)*i)), lineWidth)

def draw_o(centerX, centerY):
	pygame.draw.circle(screen, "black", (centerX, centerY), 50, 10)

def draw_x(centerX, centerY):
	pygame.draw.line(screen, "black", (centerX+50, centerY-50), (centerX-50, centerY+50), 10)
	pygame.draw.line(screen, "black", (centerX-50, centerY-50), (centerX+50, centerY+50), 10)

def print_debug():
	print(table.table[0])
	print(table.table[1])
	print(table.table[2])
	print('moveCount', table.movesCount)
	print('lastMove', table.lastmove)
	print('winner', table.winner)
	print('table_full()', table.table_full())
	print('complete', table.complete)
	print('turn', table.turn)

def game_result(winner):
	global run
	global table
	runResult = True
	while runResult:
		
		# process player input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				runResult = False
				run = False
			if event.type == pygame.K_ESCAPE:
				runResult = False
			if event.type == pygame.MOUSEBUTTONUP:
				click = pygame.mouse.get_pos()
				if againBtn.collidepoint(click):
					print('selected again')
					table = Table()
					runResult = False
				if exitBtn.collidepoint(click):
					print('selected exit')
					runResult = False
					run = False

		# logical updates
		mouse = pygame.mouse.get_pos()

		# background
		screen.fill('gray')
		pygame.draw.rect(screen, 'white', ((50, 50),(500, 500)))

		# render graphics
		font = pygame.font.SysFont('Arial', 25)
		if winner == 'd':
			img = font.render(f'It was a draw \o/ wish you luck next time!', True, "black")
		else:
			img = font.render(f'Player with "{winner.upper()}" won!!! :D', True, "black")
		screen.blit(img, (100, 100))
		againBtn = pygame.Rect(150, 400, 100, 50)
		againText = font.render('repeat', True, 'black')
		exitBtn = pygame.Rect(350, 400, 100, 50)
		exitText = font.render('exit', True, 'black')

		### adjust
		pygame.draw.rect(screen, 'red' if againBtn.collidepoint(mouse) else 'gray', againBtn)
		screen.blit(againText, (170, 410))
		pygame.draw.rect(screen, 'red' if exitBtn.collidepoint(mouse) else 'gray', exitBtn)
		screen.blit(exitText, (385, 410))

		# refresh display
		pygame.display.flip()
		clock.tick(FPS)

#game loop
while run:
	# process player input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONUP:
			table.play()

	# logical updates
	mouse = pygame.mouse.get_pos()

	# background
	screen.fill("white")
	draw_background()

	# render graphics
	table.render_moves()
	table.render_hover()

	# refresh display
	pygame.display.flip()
	
	# game is over
	if table.winner:
		# print_debug()
		game_result(table.winner)

	# tickrate
	clock.tick(FPS)

#finish
pygame.quit()
