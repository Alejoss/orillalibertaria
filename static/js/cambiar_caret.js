$('.triangulo').on('click', cambiar_caret);
function cambiar_caret(){
	console.log("llego cambiar_caret");
	var caret_span = $(this).find('.fa');
	if ($(this).hasClass('arriba')){
		caret_span.removeClass('fa-angle-up');
		caret_span.addClass('fa-angle-down');
		$(this).removeClass('arriba');
		$(this).addClass('abajo');
	}
    else if ($(this).hasClass('abajo')){
		caret_span.removeClass('fa-angle-down');
		caret_span.addClass('fa-angle-up');
		$(this).removeClass('abajo');
		$(this).addClass('arriba');
	}
}