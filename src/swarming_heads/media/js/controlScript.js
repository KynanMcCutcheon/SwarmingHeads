

/****IMPLEMENTATION****/

$(document).ready(function() {
	/****DEFINED VARIABLES (no context needed)****/

//map variables
var robPosX = width/2;
var robPosY = height/2;
var rot = 0;//this is in degrees atm
var width = 640;
var height = 320;
var robColor = 'rgb(255,0,0)';
var robSize = 10;//diameter of point


//button id's
var btn_up = '#btn_up';
var btn_right = '#btn_right';
var btn_down = '#btn_down';
var btn_left = '#btn_left';
var btn_map = '#btn_map';
var btn_chat = '#btn_chat';

//element id's
var elem_map = '#viewmap';
var elem_chat = '';

//colors
var col_btn = $(btn_up).css('background-color');
var col_btn_map = $(btn_map).css('background-color');
var col_btn_down = '#00FF00';
var col_btn_click = '#00FF00';

/**** DEFINED MAP SPECIFIC FUNCTIONS ****/

function draw() {
	var canvas = document.getElementById('robmap');
	var ctx = canvas.getContext("2d");

	ctx.fillStyle = robColor;
	ctx.fillRect (robPosX-(robSize/2), robPosY-(robSize/2), robSize, robSize);
	
	//alert('draw');
}

var map_init = function() {
	//init code here
	draw();
};

/****DEFINED FUNCTIONS****/
	
//movement
var rob_forward = function() {
	//forward code here
	//request.send(script,'EV:MOVE 0.7');
	//$(btn_up).effect("highlight", { 'color': col_btn_click }, 50);
	$(btn_up).css('background-color',col_btn_down);
};

var rob_rot_right = function() {
	//right rotation code here
	
	//$(btn_right).effect("highlight", { 'color': col_btn_click }, 50);
	$(btn_right).css('background-color',col_btn_down);
};

var rob_reverse = function() {
	//reverse code here
	//request.send(script,'EV:MOVE -0.7');
	//$(btn_down).effect("highlight", { 'color': col_btn_click }, 50);
	$(btn_down).css('background-color',col_btn_down);
};

var rob_rot_left = function() {
	//left rotation code here
	
	//$(btn_left).effect("highlight", { 'color': col_btn_click }, 50);
	$(btn_left).css('background-color',col_btn_down);
};

//mouse down and up
var ev_btn_down = function(elem) {
	//$(elem).animate({ 'background-color': col_btn_down }, 1000);
	$(elem).css('background-color',col_btn_down);
};
	
var ev_btn_up = function(elem) {
	//$(elem).animate({ 'background-color': col_btn }, 1000);
	$(elem).css('background-color',col_btn);
	alert(elem + ' pressed');
};

//button hover
var btn_hover_in = function(elem) {
	$(elem).addClass('btn_hover');	
};

var btn_hover_out = function(elem) {
	$(elem).removeClass('btn_hover');
};

//map toggling
var map_on = function() {
	//$(btn_map).effect("highlight", { 'color': '#FF0000' }, 50);
	$(btn_map).css('background-color',col_btn_down);
	$(elem_map).css("visibility","visible");
};
	
var map_off = function() {
	//$(btn_map).effect("highlight", { 'color': '#FF0000' }, 50);
	$(btn_map).css('background-color',col_btn_map);
	$(elem_map).css("visibility","hidden");
};

//chat toggling
/*
var chat_auto = function() {
	
};
	
var chat_manual = function() {
	
};*/


	/**** DEFINED FUNCTIONS (context-sensitive) ****/
	
	/**** EVENT BINDINGS ***/
	/*
	$(btn_up).hover(btn_hover_in(btn_up),btn_hover_out(btn_up));
	$(btn_right).hover(btn_hover_in(btn_right),btn_hover_out(btn_right));
	$(btn_down).hover(btn_hover_in(btn_down),btn_hover_out(btn_down));
	$(btn_left).hover(btn_hover_in(btn_left),btn_hover_out(btn_left));
	
	$(btn_up).mousedown(rob_forward(btn_up));
	$(btn_right).mousedown(rob_rot_right(btn_right));
	$(btn_down).mousedown(rob_reverse(btn_down));
	$(btn_left).mousedown(rob_rot_left(btn_left));
	
	$(btn_up).mouseup(ev_btn_up(btn_up));
	$(btn_right).mouseup(ev_btn_up(btn_right));
	$(btn_down).mouseup(ev_btn_up(btn_down));
	$(btn_left).mouseup(ev_btn_up(btn_left));
	
	$(btn_up).mouseleave(ev_btn_up(btn_up));
	$(btn_right).mouseleave(ev_btn_up(btn_right));
	$(btn_down).mouseleave(ev_btn_up(btn_down));
	$(btn_left).mouseleave(ev_btn_up(btn_left));
	*/
	$(btn_up).click(rob_forward);
	$(btn_right).click(rob_rot_right);
	$(btn_down).click(rob_reverse);
	$(btn_left).click(rob_rot_left);
	
	$(btn_map).toggle(map_on, map_off);
	//$(btn_chat).toggle(chat_auto, chat_manual);
	
	map_init();
});