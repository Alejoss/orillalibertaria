$('#modal_imagen').on('show.bs.modal', function(e){

	if ($(e.relatedTarget).parent().find('.marcar_favorito').hasClass("es_favorita")){
		nueva_imagen_fav = "es_favorita";
		$("#modal_estrella").removeClass('no_es_favorita');
	}
	else{
		nueva_imagen_fav = "no_es_favorita";
		$("#modal_estrella").removeClass('es_favorita');
	}

	var nueva_src = $(e.relatedTarget).attr('src');
	var nuevos_favoritos = $(e.relatedTarget).parent().find(".favoritos").text();
	var nuevo_counter = $(e.relatedTarget).parent().find(".forloop_counter").data('counter');
	var nuevo_id = $(e.relatedTarget).parent().find(".imagen_id").text();

	$(this).find('.modal-body > .imagen_modal').attr('src', nueva_src);
	$(this).find('.modal-header > .marcar_favorito').addClass(nueva_imagen_fav);
	$(this).find('.modal-header > #modal_favoritos').text(nuevos_favoritos);
	$(this).find('.modal-header > #modal_counter').data('counter', nuevo_counter);
	$(this).find('.modal-header > .imagen_id').text(nuevo_id);
});

function girar_puzzlepiece(puzzle_piece, direccion){
	if (direccion == "derecha"){
		if ($(puzzle_piece).hasClass("fa-rotate-90")){
			$(puzzle_piece).addClass("fa-rotate-180");	
			$(puzzle_piece).removeClass("fa-rotate-90");
		}
		else if ($(puzzle_piece).hasClass("fa-rotate-180")){
			$(puzzle_piece).addClass("fa-rotate-270");		
			$(puzzle_piece).removeClass("fa-rotate-180");
		}
		else if ($(puzzle_piece).hasClass("fa-rotate-270")){
			$(puzzle_piece).removeClass("fa-rotate-270");
		}
		else {
			$(puzzle_piece).addClass("fa-rotate-90");
		}	
	}

	else {
		if ($(puzzle_piece).hasClass("fa-rotate-90")){
			$(puzzle_piece).removeClass("fa-rotate-90");
		}
		else if ($(puzzle_piece).hasClass("fa-rotate-180")){
			$(puzzle_piece).addClass("fa-rotate-90");		
			$(puzzle_piece).removeClass("fa-rotate-180");
		}
		else if ($(puzzle_piece).hasClass("fa-rotate-270")){
			$(puzzle_piece).addClass("fa-rotate-180");
			$(puzzle_piece).removeClass("fa-rotate-270");
		}
		else {
			$(puzzle_piece).addClass("fa-rotate-270");
		}		
	}
}

$('#modal_right').on('click', function(){
	var counter_actual = parseInt($("#modal_counter").data('counter'));

	var counter_p_nuevo = "#imagen_"+String(counter_actual+1);
	if ($(counter_p_nuevo).length){
		puzzle = $("#puzzle_modal");
		girar_puzzlepiece(puzzle, "derecha");
		var counter_nuevo = $(counter_p_nuevo).data('counter');
		var src_nueva = $(counter_p_nuevo).parent().prev('.imagen').attr('src');
		var fav_nuevos = $(counter_p_nuevo).parent().find('.favoritos').text();
		var estrella_img = $(counter_p_nuevo).parent().find('.marcar_favorito');

		$("#modal_imagen").find('.imagen_modal').attr('src', src_nueva);
		$("#modal_imagen").find("#modal_favoritos").text(fav_nuevos);
		$("#modal_imagen").find("#modal_counter").data('counter', counter_nuevo);

		if (estrella_img.hasClass('es_favorita')){
			$("#modal_estrella").addClass('es_favorita');
			$("#modal_estrella").removeClass('no_es_favorita');
		}
		else if(estrella_img.hasClass('no_es_favorita')){
			$("#modal_estrella").addClass('no_es_favorita');
			$("#modal_estrella").removeClass('es_favorita');	
		}
	}
});
$('#modal_left').on('click', function(){
	var counter_actual = parseInt($("#modal_counter").data('counter'));

	var counter_p_nuevo = "#imagen_"+String(counter_actual-1);
	if ($(counter_p_nuevo).length){
		puzzle = $("#puzzle_modal");
		girar_puzzlepiece(puzzle, "izquierda");

		var counter_nuevo = $(counter_p_nuevo).data('counter');
		var src_nueva = $(counter_p_nuevo).parent().prev('.imagen').attr('src');
		var fav_nuevos = $(counter_p_nuevo).parent().find('.favoritos').text();
		var estrella_img = $(counter_p_nuevo).parent().find('.marcar_favorito');

		$("#modal_imagen").find('.imagen_modal').attr('src', src_nueva);
		$("#modal_imagen").find("#modal_favoritos").text(fav_nuevos);
		$("#modal_imagen").find("#modal_counter").data('counter', counter_nuevo);

		if (estrella_img.hasClass('es_favorita')){
			$("#modal_estrella").addClass('es_favorita');
			$("#modal_estrella").removeClass('no_es_favorita');
		}
		else if(estrella_img.hasClass('no_es_favorita')){
			$("#modal_estrella").addClass('no_es_favorita');
			$("#modal_estrella").removeClass('es_favorita');	
		}	
	}
});