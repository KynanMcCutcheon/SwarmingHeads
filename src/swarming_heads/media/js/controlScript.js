//movement functions here
var btn_move_up = function() {
	$('#btn_up').addClass('btn_click');
};

var btn_move_right = function() {
	
};

var btn_move_down = function() {
	
};

var btn_move_left = function() {
	
};

//hover button functions here
var btn_hover_in = function(elem) {
	$(elem).addClass('btn_hover');	
};

var btn_hover_out = function(elem) {
	$(elem).removeClass('btn_hover');
};

$(document).ready(function() {
	$('#btn_up').ready(function() {
		//$('#btn_up').mouseenter(btn_hover_in('#btn_up'));
		//$('#btn_up').mouseleave(btn_hover_out('#btn_up'));
		$('#btn_up').hover(btn_hover_in('#btn_up'),btn_hover_out('#btn_up'));
		$('#btn_up').click(btn_move_up);
	});
	
	
	$('#btn_right').hover(btn_hover_in('#btn_right'),btn_hover_out('#btn_right'));
	$('#btn_down').hover(btn_hover_in('#btn_down'),btn_hover_out('#btn_down'));
	$('#btn_left').hover(btn_hover_in('#btn_left'),btn_hover_out('#btn_left'));

	
	$('#btn_right').click(btn_move_right);
	$('#btn_down').click(btn_move_down);
	$('#btn_left').click(btn_move_left);
});