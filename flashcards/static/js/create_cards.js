$("#nytt_spjald").submit(function(e){
	e.preventDefault();
	
	var entry = {};
	entry.model = 'flashcards.card';
	entry.pk = null;
	entry.fields = {};
	entry.fields.deck = deck_id;
	entry.fields.question = $('#spurning').val();
	entry.fields.answer = $('#svar').val();

	$('#spjald').val(JSON.stringify([entry]));

	$.ajax({
		type: "POST",
		url: "/create/",
		data: $('#hidden').serialize(),
		success: function(data) {
			$('#tilbuin_spjold').append("<li id=\"" + data[0].pk + "\"><p>" + data[0].fields.question + "</p><p>" + data[0].fields.answer + "</p></li>");
		},
		error: function(jqXHR, status, error){
			alert("Error: " + error);
		}
	});
});