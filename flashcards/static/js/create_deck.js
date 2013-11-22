$("#nyr_stafli").submit(function(e){
	e.preventDefault();
	
	var entry = {};
	entry.model = 'flashcards.deck';
	entry.pk = null;
	entry.fields = {};
	entry.fields.name = $('#nafn').val();

	$('#stafli').val(JSON.stringify([entry]));
	$('#hidden').submit()

	//$.ajax({
	//	type: "POST",
	//	url: "/create/",
	//	data: $('#hidden').serialize(),
	//	success: function(data) {
	//		console.log(data);
	//		//window.location.href = "/create/" + data[0].pk + "/";
	//	},
	//	//error: function(jqXHR, status, error){
	//	//	alert("Error: " + error);
	//	//}
	//});
});