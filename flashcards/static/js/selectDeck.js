$('#selectDeck').change(function(){
	if ($(this).val() == "Veldu bunka")
	{
		window.location = "/";
		return;
	}
	window.location = "/" + $(this).val();
});
// Ef við erum að skoða bunka, veljum við nafn bunkans í select-tagginu.
if (deck) $('#selectDeck').val(deck.id);
