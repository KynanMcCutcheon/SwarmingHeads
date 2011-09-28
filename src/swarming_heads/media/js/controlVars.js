/**** DEFINED MAP SPECIFIC FUNCTIONS (just placeholder atm but leave here for now)****/

function draw() {
	var canvas = document.getElementById('robmap');
	var ctx = canvas.getContext("2d");

	ctx.fillStyle = robColor;
	ctx.fillRect (robPosX-(robSize/2), robPosY-(robSize/2), robSize, robSize);
	
	//alert('draw');
}
