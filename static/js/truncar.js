$(document).ready(function() {
	$('.truncate').trunk8({
	  	lines: 4,
	  	fill: '<a class="leer_mas" href="#">...leer más</a>',
	  	tooltip: false
	  });
	  $('.leer_mas').on('click', function(){
	  	$(this).parent().trunk8('revert');
	  		return false;	  	
	  });
	});