/* Js jquery para la pagina de Video.html. Un solo video con sus respuestas */
$(document).ready(function(){
	console.log("llevo video_fav");
    if ($('.estrella').hasClass("es_favorito")){
    	console.log("tiene la clase");
    	$('.estrella').addClass("dorado");
    }
});

console.log("llego video_fav")
$('.estrella').on('click', marcar_favorito);
$('.js-lazyYT').lazyYT();
$('#enviar_respuesta').on('click', sumar_respuesta);
$('#mostrar_post_padre').on('click', mostrar_post_padre);
$('#reportar_video').on('click', reportar);
$('.es_favorito').hover(function(){
    $(this).addClass("fa-star-o");
    $(this).removeClass("fa-star");
    }, function(){
    if ($(this).hasClass("es_favorito")){
        $(this).addClass("fa-star");
        $(this).removeClass("fa-star-o");
    }
});

function reportar(){
    $(this).addClass("red")
    $('#modal_reportar').removeClass("hidden");
    var p_hidden = $(this).parent().next(".hidden");
    var video_id = p_hidden.text();
    console.log(video_id);
    $.ajax({
        data: {'video_id':video_id},
        url: '/videos/denunciar_video/',
        type: 'get'
    });
}

function marcar_favorito(){
    var p_hidden = $(this).prev('.hidden');
    var video_id = p_hidden.text();
    console.log(video_id);
    var boton_estrella = $(this);
    var favoritos_recibidos_obj = boton_estrella.next('.favoritos_recibidos');
    var favoritos_recibidos = parseInt(favoritos_recibidos_obj.text());

    if (boton_estrella.hasClass('no_es_favorito')){
        $(boton_estrella).fadeOut(function(){
            $(boton_estrella).removeClass('no_es_favorito');
            $(boton_estrella).addClass('es_favorito');
	        $(boton_estrella).addClass("dorado");
            $(boton_estrella).fadeIn();
        });
        favoritos_recibidos_obj.fadeOut(function(){
        favoritos_recibidos_obj.text(favoritos_recibidos+1);
        favoritos_recibidos_obj.fadeIn();
        });
    }
    else if (boton_estrella.hasClass('es_favorito')){
        $(boton_estrella).removeClass('dorado');
        $(boton_estrella).addClass('no_es_favorito');
        favoritos_recibidos_obj.text(favoritos_recibidos-1);
    }
    $.ajax({
        data: {'video_id':video_id},
        url: '/videos/marcar_favorito/',
        type: 'get'
    });
}

function sumar_respuesta(){
	num_respuestas = parseInt($('#num_respuestas').text());
	console.log(num_respuestas)
	$('#num_respuestas').parent().effect("shake", {distance:5});
	$('#num_respuestas').text(num_respuestas+1);
}

function mostrar_post_padre(){
	$('#post_hidden').removeClass("hidden")
	$(this).addClass("hidden")
}