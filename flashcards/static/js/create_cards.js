var form_element = $("form#nytt_spjald");
var question_input = form_element.find('input#spurning');
var answer_input = form_element.find('input#svar');

console.log(question_input, answer_input);

form_element.submit( function (e) {

	createCards(e);

} );

function createCards(e)
{
	e.preventDefault();
	
	var question = $('#spurning').val();
	var answer = $('#svar').val();

	var entry = {
		model 			:'flashcards.card',
		pk 				: null,
		fields 			: {},
		fields.deck		: deck_id,
		fields.question : question,
		fields.answer   : answer
	};

	var hiddenForm = $('#hidden');
	var hiddenFormField = $('#spjald');
	hiddenFormField.val(JSON.stringify([entry]));
	var data = hiddenForm.serialize();

	$.ajax({
		type: "POST",
		url: "/create/",
		data: data,
		success: function(data) {
			prependAddedCard(data);
		},
		error: function(jqXHR, status, error){
			alert("Error: " + error);
		}
	});
}

function prependAddedCard(data)
{
	var el = $('#tilbuin_spjold')

	var id = data[0].pk;
	var question = data[0].fields.question;
	var answer = data[0].fields.answer;

	var html = "<li id=\"" + id + "\">"
	+ "<p>"
	+ question
	+ "</p>"
	+ "<p>"
	+ answer
	+ "</p></li>";

	el.prepend(html);
}