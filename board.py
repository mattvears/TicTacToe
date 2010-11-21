#!/usr/bin/env python2.5
import copy
import soul

class GameBoard(object):
	def __init__(self, size=3):
		self.winner = 0
		self.endpath = None
		self.last_turn = 0
		self.InitializeBoard(size)
		self.ComputePaths()

	def InitializeBoard(self, size):
		self.board = []
		self.size = size

		for i in range(0, size):
			self.board.append([])
			[self.board[i].append(0) for j in range(0, size)]
		
		return self.board

	def ComputePaths(self):
		self.paths = []

		# vertical and horizontal
		for row in range(0, self.size):
			vertical_path = []
			horizontal_path = []
			for col in range(0, self.size):
				vertical_path.append((row, col))
				horizontal_path.append((col, row))
		
			self.paths.append(vertical_path)
			self.paths.append(horizontal_path)
		
		# diagonal
		fwd_diag = []
		back_diag = []
		for i in range(0, self.size):
			fwd_diag.append((i, i))
			back_diag.append((i, (self.size - 1) - i))	
		
		self.paths.append(fwd_diag)
		self.paths.append(back_diag)


	def FirstTurn(self):
		for row in self.board:
			if row.count(2) > 0:
				return False
		return True

	def SetSquare(self, coords, val=2):
		row = coords[0]
		col = coords[1]
		self.board[row][col] = val
		self.last_turn = val


	@staticmethod
	def PossibleNextMoves(gameboard):
		p1 = 0
		p2 = 0	
		for row in gameboard.board:
			for col in row:
				if col == 1: p1 += 1
				if col == 2: p2 += 1
		if p1 > p2: player = 2
		else: player = 1
							
	
	
		for i in range(0, gameboard.size):
			for j in range(0, gameboard.size):
				if gameboard.board[i][j] == 0:
					gb2 = copy.deepcopy(gameboard)
					gb2.board[i][j] = player
					gb2.player = player
					yield gb2

	def NoMoreMoves(self):
		playable_paths = 0
		
		for path in self.paths:
			found1 = 0
			found2 = 0

			for coord in path:
				if self.board[coord[0]][coord[1]] == 1:
					found1 += 1
				elif self.board[coord[0]][coord[1]] == 2:
					found2 += 1
				
			if found1 == self.size:
				self.endpath = path
				self.winner = 1
			elif found2 == self.size:
				self.endpath = path	
				self.winner = 2
			if found1 > 0 and found2 == 0:
				playable_paths += 1
			elif found2 > 0 and found1 == 0:
				playable_paths += 1
					
						
		if self.winner > 0:
			return True
	
		if playable_paths == 0:
			self.tied = True	
			return True	
		else:
			self.tied = False
			return False	
		
	@staticmethod
	def MarkEndPath(gameboard):
		if gameboard.NoMoreMoves():	
			if gameboard.endpath is not None:	
				for coord in gameboard.endpath:
					gameboard.board[coord[0]][coord[1]] = 4
			return gameboard



if __name__ == "__main__":
	
	print "Test Constructor",	
	gameBoard = GameBoard()
	gameBoard = GameBoard(4)
	gameBoard = GameBoard(5)
	print "OK"


	print
	print "Test for SetSquare"
	print 	
	
	gameBoard.SetSquare((0, 0))
	gameBoard.SetSquare((1, 0))
	gameBoard.SetSquare((2, 0))
	gameBoard.SetSquare((3, 0))
	gameBoard.SetSquare((4, 0))
	print gameBoard.board

	print "Test for NoMoreMoves: ",
	
	if gameBoard.NoMoreMoves():
		if gameBoard.winner == 2:
			print "Pass."
		else:
			print "Fail, wrong winner."
	else:
		print "Fail, returned false."


	print "Test for no more moves..."
	gameBoard = GameBoard()
	gameBoard.SetSquare((0, 0), 1)
	gameBoard.SetSquare((1, 1), 2)
	if gameBoard.NoMoreMoves():
		print "FAIL!"



	print
	print "Test for PossibleNextMoves"
	print

	gameBoard = GameBoard()
	gameBoard.SetSquare((0, 0), 1)
	for move in GameBoard.PossibleNextMoves(gameBoard):
		print move.board

	print 
	print
	gameBoard = GameBoard(3)
	gameBoard.SetSquare((0,0), 2)
	gameBoard.SetSquare((1,1), 1)
	for move in GameBoard.PossibleNextMoves(gameBoard):
		print move.board	
		for move2 in GameBoard.PossibleNextMoves(move):
			print "	"  + str(move2.board)



	print
	print "First Turn Test"
	print
	gameBoard = GameBoard(3)
	print "Should be true: " + str(gameBoard.FirstTurn())
	gameBoard.SetSquare((1,1), 1)
	print "Still true: " + str(gameBoard.FirstTurn())
	gameBoard.SetSquare((1,2), 2)
	print "Now false: " + str(gameBoard.FirstTurn())
