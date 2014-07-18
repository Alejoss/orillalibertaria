$('.marcar_favorito').on('click', marcar_favorito);
$('.reportar').on('click', reportar);
$('.close').on('click', close_modal_reportar);
$('.div_marcar_portada').on('click', '.marcar_portada' , marcar_portada);
$('.es_favorita').hover(function(){
    $(this).removeClass("fa-star");
    $(this).addClass("fa-star-o");
    }, function(){
    $(this).removeClass("fa-star-o");
    $(this).addClass("fa-star");
    });

function reportar(){
    $(this).addClass("red")
    $('.modal').removeClass("hidden");
    var parent = $(this).parent();
    var p_hidden = parent.find(".hidden");
    var imagen_id = p_hidden.text();
    console.log(imagen_id);
    $.ajax({
        data: {'imagen_id':imagen_id},
        url: '/imagenes/denunciar/',
        type: 'get'
    });
}

function close_modal_reportar(){
    $('.modal').addClass("hidden");
    var flag = $('.container').find(".red");
    flag.removeClass("red");
}


function marcar_favorito(){
    var p_hidden = $(this).prev('.hidden');
    var imagen_id = p_hidden.text();
    var container = $(this).parent();
    var favoritos_recibidos_obj = container.find('.favoritos');
    var favoritos_recibidos = parseInt(favoritos_recibidos_obj.text());

    if ($(this).hasClass('no_es_favorita')){
        $(this).fadeOut(function(){
            $(this).removeClass('no_es_favorita');
            $(this).addClass('es_favorita');
            $(this).fadeIn();
        });
        favoritos_recibidos_obj.fadeOut(function(){
        favoritos_recibidos_obj.text(favoritos_recibidos+1);
        favoritos_recibidos_obj.fadeIn();
        });
    }
    else if ($(this).hasClass('es_favorita')){
         $(this).removeClass('es_favorita');
        $(this).addClass('no_es_favorita');
        favoritos_recibidos_obj.text(favoritos_recibidos-1);
    }
    $.ajax({
        data: {'imagen_id':imagen_id},
        url: '/imagenes/marcar_favorito/',
        type: 'get'
    });
}

function marcar_portada(){
    var p_hidden = $(this).parent().find(".hidden");
    var imagen_id = p_hidden.text();
    console.log(imagen_id)
    $.ajax({
        data:{'imagen_id':imagen_id},
        url: '/imagenes/marcar_portada_ajax/',
        type: 'get'
    });

    var portada_actual = $('#imagenes').find('.icono_portada');
    portada_actual.fadeOut("slow", function(){
        portada_actual.replaceWith("<span class='icon-certificate marcar_portada'></span>")
    });
    $(this).fadeOut("slow", function(){
        $(this).replaceWith(" <i class = 'icono_portada fa fa-picture-o fa-lg'> </i>")
    });
    $(this).fadeIn()
    console.log(this)
   
}
