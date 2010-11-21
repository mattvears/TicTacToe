#!/usr/bin/env python2.5
import math
import soul

from board import GameBoard
from ai import GameAI

class Game:
	KeepPlaying = 0
	Lost = 2
	Tied = 3


class ttt():
	@staticmethod
	def ListToGameBoard(lst):
		""" convert python list to the GameBoard class """
		boardsize = int(len(lst) ** .5)
		gb = GameBoard()
		gb.board = [[0 for j in range(0, boardsize)] for i in range(0, boardsize)]
	
		row = 0
		col = 0	
		for item in lst:
			gb.board[row][col] = item	
			
			col += 1
			if col >= boardsize:
				col = 0
				row += 1		
		return gb				
		
	@staticmethod
	def GameBoardToList(gameboard):
		""" convert GameBoard to list for serialization. """
		list = []	
		[[list.append(sq) for sq in row] for row in gameboard.board]				
		return list		
			
				
	@staticmethod
	def CheckBoard(board):
		gameboard = ttt.ListToGameBoard(board)
		tied = gameboard.NoMoreMoves() 
		if gameboard.winner > 0:
			return gameboard.winner	
		elif tied:
			return Game.Tied
		else:
			return Game.KeepPlaying


	@staticmethod
	def GetNextAIMove(board):
		gb = ttt.ListToGameBoard(board)
		ai = GameAI(gb)
		if ai.EndState is not None:
			return ttt.GameBoardToList(ai.EndState)
		else:
			return ttt.GameBoardToList(gb)



