$(document).ready(function(){
$("#beta_password").keyup(function(){
	if ($(this).val() === 'bastiat'){
		$("#beta_form").fadeOut(function(){$(this).addClass("hidden")});
		$("#facebook_twitter").removeClass("hidden");
	}
});
});
