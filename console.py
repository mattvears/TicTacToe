#!/usr/bin/env python2.5
from ttt2 import ttt, Game
from board import GameBoard

board = [0,0,0,0,0,0,0,0,0]
game_state = 0


def DrawPos(pos_data, pos):
	if pos_data == 1:
		return '\033[94m' + 'X' + '\033[0m'
	elif pos_data == 2:
		return '\033[92m' + 'O' + '\033[0m'
	elif pos_data == 3:
		return '\033[95m' + 'X' + '\033[0m'
	elif pos_data == 4:
		return '\033[95m' + 'O' + '\033[0m'
	else:
		return str(pos)


def DrawBoard(board):
	j = 0
	for i in range(0,3):
		print ''.join([
			DrawPos(board[j],j), ' | ',
			DrawPos(board[j+1],j+1), ' | ',
			DrawPos(board[j+2],j+2)])

		if i < 2:
			print '----------'
		j += 3

if __name__ == '__main__':
	while game_state is 0:
		print
		DrawBoard(board)
		print
		
		next_pos = raw_input("Next move? ")
		
		if board[int(next_pos)] is 0:
			board[int(next_pos)] = 1
	
			game_state = ttt.CheckBoard(board)
			if game_state is 0:
				board = ttt.GetNextAIMove(board)
				game_state = ttt.CheckBoard(board)
				print "game state: " + str(game_state) + ", board: " + str(board)	
		else:
			print "That spot is occupied."
	
	gb = GameBoard.MarkEndPath(ttt.ListToGameBoard(board))
	DrawBoard(ttt.GameBoardToList(gb))
	
	if game_state is Game.Lost: 
		print "You Lose"
	elif game_state is Game.Tied:
		print "Tied"
