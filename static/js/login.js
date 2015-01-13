$("#puzzle_posts").on('click', cambiar_post);
$("#puzzle_frases").on('click', cambiar_frases);
$("#puzzle_imagenes").on('click', cambiar_imagenes);

function girar_puzzlepiece(puzzle_piece){
	$(puzzle_piece).fadeOut(function(){
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
	}).delay(500);
	$(puzzle_piece).fadeIn();
}
function cambiar_imagenes(){
	var owl = $("#owl-demo");
	owl.trigger('owl.next');
	girar_puzzlepiece($("#puzzle_imagenes"))
}
function cambiar_post(){
	var posts_num = $("#posts_num").text();

	if (posts_num == 0){
		console.log($("#post_1"));
		nuevo_html = $("#post_1").html();
		console.log(nuevo_html);
		$("#div_posts").html(nuevo_html);
		$("#posts_num").text("1");
	}
	else if (posts_num == 1){
		console.log($("#post_2"));
		nuevo_html = $("#post_2").html();
		console.log(nuevo_html);
		$("#div_posts").html(nuevo_html);
		$("#posts_num").text("2");
	}
	else if (posts_num == 2){
		console.log($("#post_0"));
		nuevo_html = $("#post_0").html();
		console.log(nuevo_html);
		$("#div_posts").html(nuevo_html);
		$("#posts_num").text("0");
	}

	girar_puzzlepiece($("#puzzle_posts"))
}
function cambiar_frases(){
	var frases_num = $("#frases_num").text();
	if (frases_num == 0){
		nueva_frase_1 = $("#cita_2").text();
		nueva_descripcion_1 = $("#cita_2_autor").text()
		nueva_frase_2 = $("#cita_3").text();
		nueva_descripcion_2 = $("#cita_3_autor").text()
		$("#cita_3_autor").text();
		$("#frases_num").text("1");
	}
	else if (frases_num == 1){
		nueva_frase_1 = $("#cita_4").text()
		nueva_descripcion_1 = $("#cita_4_autor").text()
		nueva_frase_2 = $("#cita_5").text()
		nueva_descripcion_2 = $("#cita_5_autor").text()
		$("#frases_num").text("2");
	}
	else if (frases_num == 2){
		nueva_frase_1 = $("#cita_0").text()
		nueva_descripcion_1 = $("#cita_0_autor").text()
		nueva_frase_2 = $("#cita_1").text()
		nueva_descripcion_2 = $("#cita_1_autor").text()
		$("#frases_num").text("0");
	}
	$("#text_frase_1").text(nueva_frase_1);
	$("#descripcion_frase_1").text(nueva_descripcion_1);
	$("#text_frase_2").text(nueva_frase_2);
	$("#descripcion_frase_2").text(nueva_descripcion_2);

	girar_puzzlepiece($("#puzzle_frases"))
}
