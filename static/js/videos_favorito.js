/* Js jquery para la pagina videos_tema.html, los videos de tema */

$(document).ready(function(){
    $('.control_votos').each(function(){
        var referencia = $(this).find('.estrella');
        if (referencia.hasClass("es_favorito")){
            referencia.addClass("btn-warning");
            referencia.removeClass("btn-default");
        }
    });
});

$('.estrella').on('click', marcar_favorito);
$('.es_favorito').hover(function(){
    $(this).addClass("btn-default");
    $(this).removeClass("btn-warning");
    }, function(){
        if ($(this).hasClass("es_favorito")){
            $(this).addClass("btn-warning");
            $(this).removeClass("btn-default");    
        }
    });

function marcar_favorito(){
    var p_hidden = $(this).prev('.hidden');
    var video_id = p_hidden.text();
    var boton_estrella = $(this);
    var estrella_icono_interno = boton_estrella.find('.fa');
    var favoritos_recibidos_btn = boton_estrella.next('.puntaje');
    var favoritos_recibidos_obj = favoritos_recibidos_btn.find('.numero_puntaje');
    var favoritos_recibidos = parseInt(favoritos_recibidos_obj.text());

    if (boton_estrella.hasClass('no_es_favorito')){
        $(boton_estrella).fadeOut(function(){
            $(boton_estrella).removeClass('no_es_favorito');
            $(boton_estrella).addClass('es_favorito');
            $(boton_estrella).fadeIn();
        });
        favoritos_recibidos_obj.fadeOut(function(){
        favoritos_recibidos_obj.text(favoritos_recibidos+1);
        $(boton_estrella).removeClass("btn-default");
        $(boton_estrella).addClass("btn-warning");
        favoritos_recibidos_obj.fadeIn();
        });
    }
    else if (boton_estrella.hasClass('es_favorito')){
        $(boton_estrella).removeClass('es_favorito');
        $(boton_estrella).removeClass("btn-warning");
        $(boton_estrella).addClass("btn-default");
        $(boton_estrella).addClass('no_es_favorito');
        favoritos_recibidos_obj.text(favoritos_recibidos-1);
    }
    $.ajax({
        data: {'video_id':video_id},
        url: '/videos/marcar_favorito/',
        type: 'get'
    });
}