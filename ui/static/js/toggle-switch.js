$(document).ready(function(){
	setTimeout(function(){ 
		var elem = $('.js-switch');
		for(var i in elem){
			new Switchery(elem[i]);
		}
	}, 5000);
	// var elem = document.querySelector('.js-switch');

});