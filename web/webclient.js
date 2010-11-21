TicTacToe = {};
TicTacToe.GameNumber = 0;
TicTacToe.GameStatus = 0;
TicTacToe.Thinking = false;
TicTacToe.Drawing = false;
TicTacToe.Mobile = false;
TicTacToe.Board = "000000000";
TicTacToe.SquareNumberRegex = new RegExp(".*?(sq)(\\d+)", ["i"]); 
TicTacToe.WinningPaths = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
TicTacToe.Winner = 0;
TicTacToe.SimulationInterval = null;

String.prototype.Replace = function(index, char) {
	return this.substr(0, index) + char + this.substr(index+char.length);
};

$.fn.SquareNumber = function() {
	var classes = this.attr('class');
	var m = TicTacToe.SquareNumberRegex.exec(classes);
	return parseInt(m[2], 10);
};


TicTacToe.Gametick = function() {
	if (parseInt(TicTacToe.GameStatus, 10) === 0) {
		TicTacToe.DrawBoard();
	} else { 
		TicTacToe.DrawBoard();
	
		if (TicTacToe.Mobile !== true) {		
			if (TicTacToe.GameNumber < 49) {
				var game = $("#game" + TicTacToe.GameNumber);
				game.css('opacity', 0.8);
				game.animate({opacity: 0.4}, 10000);
				
				// start new game
				TicTacToe.GameNumber += 1;
				TicTacToe.GameStatus = 0;
				TicTacToe.Board = "000000000";
				TicTacToe.DrawBoard();
			} else {
				clearInterval(TicTacToe.SimulationInterval);
				$('.sq').animate({opacity: 0}, 3000);
				$('.gameboard').css('background-color', 'orangered');
				$('.gameboard').animate({opacity: 1}, 1000);
			}
		} else {
			// mobile version!
			var msg = "";
			if (TicTacToe.GameStatus == 3) { 
				msg = "<span class='draw'>tied</span>";
			} else if (TicTacToe.GameStatus == 2) {
				msg = "<span class='lost'>You Lost! :(</span>";
			}

			$("#gamestatus").html("Game over! " + msg + " <a href='javascript:location.reload(true)'>Play Again?</a>");
		}
	}
};



TicTacToe.GetNextAIMove = function() {
	TicTacToe.Thinking = true;
	$.ajax({
		type: 'GET',
		dataType: 'jsonp',
		url: 'http://beta.confusiontechnology.com/TicTacToe/server.py/' + TicTacToe.Board + '/',
		success: function(data) {
			$('.loader').remove();
			TicTacToe.Board = data.b;
			TicTacToe.GameStatus = data.r;
			TicTacToe.Gametick();
			TicTacToe.Thinking = false;
		}
	});
};

TicTacToe.ShowLoader = function () {
	$('#game' + TicTacToe.GameNumber).append("<div class='loader'><img src='./img/ajax-loader.gif' /></div>");
};

TicTacToe.ClickSquare = function() {
	var this_square = $(this);
	if (TicTacToe.Mobile === false) {
		TicTacToe.ShowLoader();
	}
	TicTacToe.Board = TicTacToe.Board.Replace(this_square.SquareNumber(), '1');
	TicTacToe.GetNextAIMove();
};

TicTacToe.HoverOn = function() {
	$(this).addClass('e_hov');
};

TicTacToe.HoverOff = function() {
	$(this).removeClass('e_hov');
};

TicTacToe.DrawBoard = function() {
	TicTacToe.Drawing = true;
	var currentGameString = "game" + TicTacToe.GameNumber;
	var draw_board = $("<div></div>").addClass("gameboard").attr("id", currentGameString).css('display', 'none');
	
	
	var emptyBoard = true;
	for (var i = 0; i < 9; i++)	
	{
		var sq_type = TicTacToe.Board[i];
		var new_sq = $("<div>&nbsp;</div>").addClass('sq' + i).addClass('sq');
		
		switch (sq_type)
		{
			case "0": // empty
				new_sq.addClass('empty').hover(TicTacToe.HoverOn, TicTacToe.HoverOff);
				break;
			case "1": // X
				new_sq.addClass('X').html('X');
				emptyBoard = false;
				break;
			case "2": // O
				new_sq.addClass('O').html('O');
				emptyBoard = false;
				break;
			case "4": // Winning O
				new_sq.addClass('rO').html('O');
				emptyBoard = false;
				break;
		}

		if (emptyBoard) {
			draw_board.append(new_sq).fadeIn(); 
		}
		else {
			draw_board.append(new_sq).css('display', 'block');
		}
	}

	$('#' + currentGameString).remove();
	$('body').prepend(draw_board);
	TicTacToe.Drawing = false;
};




TicTacToe.GetWinner = function(board){
	for (var pathNum in TicTacToe.WinningPaths) {
		if (!isNaN(parseInt(pathNum, 10))) {
			var found1 = 0;
			var found2 = 0;
	
			var path = TicTacToe.WinningPaths[pathNum];
			for (var pathCoordIndex = 0; pathCoordIndex < 3; pathCoordIndex++) {
				var pathCoord = path[pathCoordIndex];
	
				if (board[pathCoord] === "1") {
					found1 += 1;
				} else if (board[pathCoord] === "2") {
					found2 += 1;
				}
			}
	
			if (found1 == 3) {
				return 1;
			} else if (found2 == 3) {
				return 2;
			}
		}
	}
	return 0;
};


TicTacToe.NoMoreMoves = function(board) {
	var winner = TicTacToe.GetWinner(board);
	if (winner > 0) {
		return true;
	} else {
		if (board.indexOf("0") == -1) {
			return true;
		} else {
			return false;
		}
	}
};


TicTacToe.NextMoves = function(player, board) {
	var retv = [];
	for (var i = 0; i < 9 ; i++) {
		if (board[i] === '0') {
			var newBoard = board;
			newBoard = newBoard.Replace(parseInt(i, 10), player);
			retv.push(newBoard);
		}
	}
	return retv;
};

TicTacToe.MiniMax = function(player, gameboard, alpha, beta, depth, max_depth) {
	if (TicTacToe.NoMoreMoves(gameboard) || depth > max_depth) {
		winner = TicTacToe.GetWinner(gameboard);
		if (winner == 1) {
			return 1;
		} else if (winner == 2) {
			return -1;
		} else { 
			return 0;
		}
	} else {
		var best = null;
		var best_board = null;
		var moves = null;
		var nextMove = null;
		var i = 0;

		if (player == 1) {
			moves = TicTacToe.NextMoves('1', gameboard);
			for (i in moves) {
				if (!isNaN(parseInt(i, 10))) {
					nextMove = moves[i];
					score = TicTacToe.MiniMax(2, nextMove, alpha, beta, depth+1, max_depth);
					if (score > alpha) {
						alpha = score;
						best_board = nextMove;
					}
					if (alpha >= beta) {
						return alpha;
					}
				}
			}
			if (depth === 0) {
				TicTacToe.NextMove = best_board;
			}	
			return alpha;
		}	
		else if (player == 2) {
			moves = TicTacToe.NextMoves('2', gameboard);
			for (i in moves) {
				if (!isNaN(parseInt(i, 10))) {
					nextMove = moves[i];
					score = TicTacToe.MiniMax(1, nextMove, alpha, beta, depth+1, max_depth);
					if (score < beta) {
						beta = score;
						best_board = nextMove;
					}
					if (alpha >= beta) {
						return beta;
					}
				}
			}
			return beta;
		}
	}
};


TicTacToe.GetPlayer1Move = function() {
	if (TicTacToe.Thinking === false && TicTacToe.Drawing === false) {
		var game = $("#game" + TicTacToe.GameNumber);
		if (game.find('.empty').length == 9) {
			var nextmove = Math.floor(Math.random() * 9);
			TicTacToe.Board = TicTacToe.Board.Replace(nextmove, '1');
		} else {
			TicTacToe.MiniMax(1, TicTacToe.Board, -Infinity, Infinity, 0, 9);
			TicTacToe.Board = TicTacToe.NextMove;
		}
		
		TicTacToe.DrawBoard();
		TicTacToe.ShowLoader();
		TicTacToe.GetNextAIMove();
	}
};





$(document).ready(function() {
	$('.empty').live('click', TicTacToe.ClickSquare);
	$('.X, .O').die('click', TicTacToe.ClickSquare);	
	$('#skip').click(function () {
		$("#skip").after("<img src='./img/small-loader.gif' class='small-loader' />");
		TicTacToe.SimulationInterval = setInterval(TicTacToe.GetPlayer1Move, 1000);
	});
});


