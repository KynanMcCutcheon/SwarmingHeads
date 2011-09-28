/****VARIABLES****/

//button id's
var btn_up = '#btn_up';
var btn_right = '#btn_right';
var btn_down = '#btn_down';
var btn_left = '#btn_left';
var btn_map = '#btn_map';
var btn_chat = '#btn_chat';

//element id's
var elem_map = '#viewmap';
var elem_chat = '';//placeholder variable in case we need it. remove when it is confirmed to be unnecessary

//const message strings
/*
NOTE:
If anyone is planning to somehow get these messages from a text file, 
please use a json or regular request object to send the data to this file or some other method to
populate this area without moving all of this code to a html file.  It would just be
amazingly cumbersome to go around a bunch of code and isn't professionally tidy.
This kind of code should always be separated from html files as it is easier to manage.
Of course if someone has a better idea please share it so more progress can be made.

Also it would be a good idea to request info from here or add a script at the index page before this js file.
Why?  We can personalise the actual messages to be sent at the client browser so the string building is
done here.  We then just send the correct messages to the message parsing script handled by daniel.
Any feedback about this would be most appreciated.
*/

/*
change these strings to the proper formatted messages.  If you are reading this Daniel and already know
the exact message format by heart, could you fill them in?  i made the script this way so any changes you make don't affect the rest of the script.
*/
var msg_chat_auto_true = 'SET_AUTO 1';
var msg_chat_auto_false = 'SET_AUTO 0';
var rob_forward = 'RB_S 0.5';
var rob_reverse = 'RB_S -0.5';
var rob_stop = 'RB_S 0.0';
var rob_rot_left = 'RB_T -3.0';
var rob_rot_right = 'RB_T 3.0';
var rob_rot_stop = 'RB_T 0.0';

//map variables
var width = 640;
var height = 320;
var robPosX = width/2;
var robPosY = height/2;
var rot = 0;//this is in degrees atm
var robColor = 'rgb(255,0,0)';
var robSize = 10;//diameter of point

/****IMPLEMENTATION****/

$(document).ready(function() {
	//colors
	var col_btn = $(btn_up).css('background-color');
	var col_btn_map = $(btn_map).css('background-color');
	var col_btn_chat = $(btn_chat).css('background-color');
	var col_btn_hover = '#666666';
	var col_btn_down = '#00FF00';
	var col_btn_error = '#00FF00';
	var col_btn_click = '#00FF00';
	
	//mouse variables
	var btnpressed = false;
	var elempressed = '';
	
	//mousedown code (empty for now)
	$(document).mousedown(function() {
		//leaving it here just in case, but will be removed once everything is finalised
	});
	
	//mouse up code
	$(document).mouseup(function() {
		if(btnpressed == true) {//just to avoid accidental firings
			switch(elempressed) {
				case btn_up:
				case btn_down:
					//request.send(movescript, rob_stop); (just pseudocode placeholder. change to actual code)
					break;
				case btn_left:
				case btn_right:
					//request.send(movescript, rob_rot_stop); (just pseudocode placeholder. change to actual code)
					break;
			}
			
			$(elempressed).css('background-color',col_btn);
			btnpressed = false;
		}
	});
	
	//up button down code
	$(btn_up).mousedown(function() {
		//request.send(parsescript, rob_forward); (pseudocode. change to actual code)
		elempressed = btn_up;
		//if robot has no errors when moving
		$(this).css('background-color',col_btn_down);
		//else
		//$(this).css('background-color',col_btn_error);
		btnpressed = true;
	});
	
	//right button down code
	$(btn_right).mousedown(function() {
		//request.send(parsescript, rob_rot_right); (pseudocode. change to actual code)
		elempressed = btn_right;
		//if robot has no errors when moving
		$(this).css('background-color',col_btn_down);
		//else
		//$(this).css('background-color',col_btn_error);
		btnpressed = true;
	});
	
	//down button down code
	$(btn_down).mousedown(function() {
		//request.send(parsescript, rob_reverse); (pseudocode. change to actual code)
		elempressed = btn_down;
		//if robot has no errors when moving
		$(this).css('background-color',col_btn_down);
		//else
		//$(this).css('background-color',col_btn_error);
		btnpressed = true;
	});
	
	//left button down code
	$(btn_left).mousedown(function() {
		//request.send(parsescript, rob_rot_left); (pseudocode. change to actual code)
		elempressed = btn_left;
		//if robot has no errors when moving
		$(this).css('background-color',col_btn_down);
		//else
		//$(this).css('background-color',col_btn_error);
		btnpressed = true;
	});
	
	//map toggle code
	$(btn_map).toggle(function() {
		$(btn_map).css('background-color',col_btn_down);
		$(elem_map).css("visibility","visible");
	}, function() {
		$(btn_map).css('background-color',col_btn_map);
		$(elem_map).css("visibility","hidden");
	});
	
	//chat toggle code
	$(btn_chat).toggle(function() {
		//request.send(parsescript, msg_chat_auto_true); (pseudocode. change to actual code)
		$(btn_chat).css('background-color',col_btn_down);
	}, function() {
		//request.send(parsescript, msg_chat_auto_false); (pseudocode. change to actual code)
		$(btn_chat).css('background-color',col_btn_chat);
	});
});