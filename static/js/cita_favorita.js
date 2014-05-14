$('.reportar_cita').on('click', reportar);
$('.close').on('click', close_modal_reportar);
$('.dorado').hover(function(){
    $(this).removeClass("fa-star");
    $(this).addClass("fa-star-o");
    }, function(){
    $(this).removeClass("fa-star-o");
    $(this).addClass("fa-star");
    });

$(document).ready(function(){
	$('.marcar_favorito').each(function(){
		if ($(this).hasClass("dorado")){
			$(this).removeClass("fa-star-o");
			$(this).addClass("fa-star");
		}
	});
});

function reportar(){
    $(this).addClass("red")
    $('#modal_reportar').removeClass("hidden");
    var p_hidden = $(this).parent().next(".hidden");
    var frase_id = p_hidden.text();
    console.log(frase_id);
    $.ajax({
        data: {'frase_id':frase_id},
        url: '/citas/denunciar_cita/',
        type: 'get'
    });
}

function close_modal_reportar(){
    $('.modal').addClass("hidden");
    var flag = $('.container').find(".red");
    flag.removeClass("red");
}


$('.marcar_favorito').on('click', marcar_favorito);
function marcar_favorito(){
	console.log("marco favorito");
	p_hidden = $(this).prev('.hidden');
	frase_id = p_hidden.text();
	$.ajax({
		data: {'frase_id':frase_id},
		url: '/citas/marcar_favorito/',
		type: 'get'
	});
	var favoritos_recibidos_obj = $(this).next('.cita_favoritos');
	var favoritos_recibidos = parseInt(favoritos_recibidos_obj.text())
	if ($(this).hasClass('dorado')){
		favoritos_recibidos_obj.text(favoritos_recibidos-1);
		$(this).removeClass('fa-star');
		$(this).addClass('fa-star-o');
		$(this).removeClass('dorado');
	}
	else if ($(this).hasClass('fa-star-o')){
		$(this).fadeOut(function(){
			$(this).addClass('fa-star');
			$(this).removeClass('fa-star-o');
			$(this).addClass('dorado');
		});
		$(this).fadeIn();
		favoritos_recibidos_obj.fadeOut(function(){	
		favoritos_recibidos_obj.text(favoritos_recibidos+1);
		favoritos_recibidos_obj.fadeIn();
		});
	}
}