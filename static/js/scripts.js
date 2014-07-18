$(document).ready(function(){
	$('#vote-up').click(function(){
		$(this).removeClass("btn-default").addClass("btn-warning")
	})
	$('.texto').each(function(){
		var inner_text = $(this).text();
		$(this).text(inner_text.replace(/(?:\r\n|\r|\n)/g, '<br />'));
		$(this).text(inner_text.replace(/^(?:<br\s\/>)+/g, ''));
		});
})