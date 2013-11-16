var form_element = $("form#nytt_spjald");
var question_input = form_element.find('input#spurning');
var answer_input = form_element.find('input#svar');

var enter_keycode = 13;

$(question_input).on('keydown', function (e) {
	if(e.which === enter_keycode)
	{
		e.preventDefault();
		answer_input.focus();
	}
});

$(answer_input).on('keydown', function (e) {
	if(e.which === enter_keycode)
	{
		question_input.focus();
	}
});

var tilbuid_element = $("#tilbuin_spjold");

//tilbuid_element.delegate()

form_element.submit( function (e) {
	createCards(e, form_element);
});

function createCards(e, form_element)
{
	e.preventDefault();
	
	var question = $('#spurning').val();
	var answer = $('#svar').val();

	var entry = {
		model 			:'flashcards.card',
		pk 				: null,
		fields 			: {
			deck		: deck_id,
			question 	: question,
			answer   	: answer
		}
		
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
			// Add the newly created card to the DOM
			// and clear the form
			prependAddedCard(data);
			clearForm(form_element);
		},
		error: function(jqXHR, status, error){
			// Do not clear form if server does not 
			// save the card
			alert("Error: " + error);
		}
	});
}

function clearForm(el) {
	$(el).find('input[type=text]').val("");
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