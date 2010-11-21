// override the value set in webclient.js
TicTacToe.Mobile = true;

// mobile version specifics
$(document).ready(function() {
	// show indication that the page is doing something. 
	$('.empty').live('click', function() {
		$(this).css('background-color', '#ff9900');	
		$('body').append("<div class='loader'><img src='./img/ajax-loader.gif' /></div>");	
	});
});
