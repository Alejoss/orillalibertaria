$('.marcar_favorito').on('click', marcar_favorito);
$('.reportar').on('click', reportar);
$('#close_modal_reportar').on('click', close_modal_reportar);
$('.div_imagen').on('click', '.marcar_portada' , marcar_portada);
$('.es_favorita').hover(function(){
    $(this).removeClass("fa-star");
    $(this).addClass("fa-star-o");
    }, function(){
    $(this).removeClass("fa-star-o");
    $(this).addClass("fa-star");
    });

function reportar(){
    $(this).addClass("red");
    $('#modal_reportar').modal('show');
    var imagen_id = $(this).parent().find('.imagen_id').text();
    $.ajax({
        data: {'imagen_id':imagen_id},
        url: '/imagenes/denunciar/',
        type: 'get'
    });
}

function close_modal_reportar(){
    $('#modal_reportar').addClass("hidden");
    var flag = $('.container').find(".red");
    flag.removeClass("red");
}


function marcar_favorito(){
    var div_parent = $(this).parent();
    var p_hidden = div_parent.find('.imagen_id');
    var imagen_id = p_hidden.text();
    var favoritos_recibidos_obj = div_parent.find('.favoritos');
    var favoritos_recibidos = parseInt(favoritos_recibidos_obj.text());

    if ($(this).hasClass('no_es_favorita')){
        console.log("no es favorita")
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
        console.log("es favorita")
        $(this).removeClass('es_favorita');
        $(this).addClass('no_es_favorita');
        favoritos_recibidos_obj.text(favoritos_recibidos-1);
    }

    if ($(div_parent).hasClass('modal-header')){
        console.log("activado desde modal");
        var counter_actual = div_parent.find('#modal_counter').data('counter');
        console.log("counter_actual:");
        console.log(counter_actual);
        var counter_1 = "#imagen_"+counter_actual;
        console.log("counter_1:");
        console.log(counter_1);
        var counter_img_fav = $(counter_1);
        console.log("counter_img_fav:");
        console.log(counter_img_fav);
        var estrella_img_fav = counter_img_fav.parent().find('.marcar_favorito');
        console.log("estrella_img_fav:");
        console.log(estrella_img_fav);
        var favoritos_img_fav = counter_img_fav.parent().find('.favoritos');
        console.log("favoritos_img_fav");
        console.log(estrella_img_fav);

        if ($(estrella_img_fav).hasClass('no_es_favorita')){
            console.log("No es favorita fuera del modal")
            $(estrella_img_fav).removeClass('no_es_favorita');
            $(estrella_img_fav).addClass('es_favorita');
            $(favoritos_img_fav).text(favoritos_recibidos+1);
        }
        else if ($(estrella_img_fav).hasClass('es_favorita')){
            console.log("Es favorita fuera del modal")
            $(estrella_img_fav).removeClass('es_favorita');
            $(estrella_img_fav).addClass('no_es_favorita');
            $(favoritos_img_fav).text(favoritos_recibidos-1);   
        }
    }

    $.ajax({
        data: {'imagen_id':imagen_id},
        url: '/imagenes/marcar_favorito/',
        type: 'get'
    });
}

function marcar_portada(){
    var imagen_id = $(this).parent().find(".imagen_id").text();
    $.ajax({
        data:{'imagen_id':imagen_id},
        url: '/imagenes/marcar_portada_ajax/',
        type: 'get'
    });

    var portada_actual = $(".icono_portada");
    console.log(portada_actual);
    portada_actual.addClass("fa-certificate marcar_portada");
    portada_actual.removeClass("fa-picture-o fa-lg icono_portada");
    $(this).fadeOut("slow", function(){
        $(this).addClass("fa-picture-o fa-lg icono_portada");
        $(this).removeClass("fa-certificate marcar_portada");
    });
    $(this).fadeIn()  
}
