$('ul.stack').click(function (e) {
	console.log(e.target.id);
});

$('#selectDeck').change(function(){
	if ($(this).val() == "Veldu bunka")
	{
		window.location = "/";
		return;
	}
	window.location = "/" + $(this).val() + "/";
});
// Ef við erum að skoða bunka, veljum við nafn bunkans í select-tagginu.
if (deck) $('.stack').val(deck.id);
