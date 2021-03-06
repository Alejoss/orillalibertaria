
$(document).ready(function(){
	$('.control_votos').each(function(){
		var referencia = $(this).find('.numero_puntaje');
		if (referencia.hasClass("voted-up")){
			$(this).find('.vote-up').toggleClass("btn-warning");
			$(this).find('.vote-down').removeClass("btn-warning");
		}
		else if (referencia.hasClass("voted-down")){
			$(this).find('.vote-down').toggleClass("btn-warning");
			$(this).find('.vote-up').removeClass("btn-warning");
		}
		else if (referencia.hasClass("no-vote")){
			$(this).find('.vote-down').removeClass("btn-warning");
			$(this).find('.vote-up').removeClass("btn-warning");
		}
		else if (referencia.hasClass("propio_post")){
			$(this).find('.vote-down').addClass("disabled");
			$(this).find('.vote-up').addClass("disabled");
		}
	});
});

$('.vote-up').on('click', vote_up);
$('.vote-down').on('click', vote_down);
$('#enviar_respuesta').on('click', sumar_respuesta);
$('#mostrar_post_padre').on('click', mostrar_post_padre);

function sumar_respuesta(){
	num_respuestas = parseInt($('#num_respuestas').text());
	$('#num_respuestas').parent().effect("shake", {distance:5});
	$('#num_respuestas').text(num_respuestas+1);
}

function mostrar_post_padre(){
	$('#post_hidden').removeClass("hidden")
	$(this).addClass("hidden")
}
function vote_up(){
	var $control = $(this).parent();
	var puntaje_obj = $control.find('.numero_puntaje');

	if ( puntaje_obj.not("propio_post")){

		var puntaje = parseInt($control.find('.numero_puntaje').text());
		var nuevo_puntaje = puntaje;
		var post_id = $control.find('.vote-id').text();
		$(this).toggleClass("btn-warning");
		$control.children(".vote-down").removeClass("btn-warning");

		if ( puntaje_obj.hasClass("voted-down"))
		{
			var nuevo_puntaje = puntaje + 2;
			puntaje_obj.removeClass("voted-down");
			puntaje_obj.addClass("voted-up");

			$.ajax({
			data: {'post_id':post_id},
			url: '/temas/vote_up_ajax/',
			type: 'get',
			});
		}
		
		else if ( puntaje_obj.hasClass("no-vote") )
		{
			var nuevo_puntaje = puntaje + 1;
			puntaje_obj.removeClass("no-vote");
			puntaje_obj.addClass("voted-up");

			$.ajax({
			data: {'post_id':post_id},
			url: '/temas/vote_up_ajax/',
			type: 'get',
			});
		}

		else if (puntaje_obj.hasClass("voted-up"))
		{
			var nuevo_puntaje = puntaje - 1;
			puntaje_obj.removeClass("voted-up");
			puntaje_obj.addClass("no-vote");

			$.ajax({
				data: {'post_id':post_id},
				url: '/temas/remover_voto_ajax/',
				type: 'get',
			});
		}

	}

	puntaje_obj.text(nuevo_puntaje);

}

function vote_down(){
	
	var $control = $(this).parent();
	var puntaje_obj = $control.find('.numero_puntaje');		
	
	if (puntaje_obj.not("propio_post")){

		$(this).toggleClass("btn-warning");
		$control.children(".vote-up").removeClass("btn-warning");
		var puntaje = parseInt($control.find('.numero_puntaje').text(), 10);
		var nuevo_puntaje = puntaje;
		var post_id = $control.find('.vote-id').text();

		if ( puntaje_obj.hasClass("voted-up"))
		{
			var nuevo_puntaje = puntaje - 2;
			puntaje_obj.removeClass("voted-up");
			puntaje_obj.addClass("voted-down");

			$.ajax({
				data: {'post_id':post_id},
				url: '/temas/vote_down_ajax/',
				type: 'get',
			});
		}
		else if (puntaje_obj.hasClass("no-vote")){

			var nuevo_puntaje = puntaje -1;
			puntaje_obj.removeClass("no-vote");
			puntaje_obj.addClass("voted-down");

			$.ajax({
				data: {'post_id':post_id},
				url: '/temas/vote_down_ajax/',
				type: 'get',
			});
		}
		else if (puntaje_obj.hasClass("voted-down")){

			var nuevo_puntaje = puntaje +1;
			puntaje_obj.removeClass("voted-down");
			puntaje_obj.addClass("no-vote");

			$.ajax({
				data: {'post_id':post_id},
				url: '/temas/remover_voto_ajax/',
				type: 'get',
			});
		}
	}

	puntaje_obj.html(nuevo_puntaje);

}