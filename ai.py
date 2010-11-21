#!/usr/bin/env python2.5
from board import GameBoard
import copy
import soul

	
class GameAI():
	def __init__(self, gameboard):
		self.StartState = gameboard
		self.EndState = None
		self.StartState.player = 2
		self.Minimax(2, self.StartState)
				
	def Minimax(self, player, gameboard, alpha=float("-Inf"), beta=float("Inf"), depth=0, max_depth=5):
		if gameboard.NoMoreMoves() or depth > max_depth:
			if gameboard.winner == 1:
				return -1
			if gameboard.winner == 2:
				return 1
			else:	
				return 0;

		else:
			best = None
			best_board = None
			if player == 2:
				for board in GameBoard.PossibleNextMoves(gameboard): 
					score = self.Minimax(1, board, alpha, beta, depth+1, max_depth)
					if score > alpha:
						alpha = score 
						best_board = copy.deepcopy(board)
					if alpha >= beta:
						return alpha
				if depth == 0:
					self.EndState = best_board	
				return alpha	

			elif player == 1:
				for board in GameBoard.PossibleNextMoves(gameboard):
					score = self.Minimax(2, board, alpha, beta, depth+1, max_depth)
					if score < beta:
						beta = score
						best_board = copy.deepcopy(board)
					if alpha >= beta:
						return beta	
				return beta		
