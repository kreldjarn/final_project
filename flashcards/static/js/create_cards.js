// Variables
// =============================================================
var form_element = $("form#nytt_spjald");
var question_input = form_element.find('input#spurning');
var answer_input = form_element.find('input#svar');

var enter_keycode = 13;

// Event Binding
// =============================================================
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
tilbuid_element.delegate('li input', 'focus', function (e) { $(e.target).addClass('edit'); });
tilbuid_element.delegate('li input', 'blur', function (e) { $(e.target).removeClass('edit'); editCard(e, true); });
tilbuid_element.delegate('li input[type="checkbox"]', 'change', function(e) { editCard(e, true); });
tilbuid_element.delegate('li button.delete', 'click', function(e) { deactivate(e); console.log("Delete: " + e.target) });
tilbuid_element.delegate('form', 'keydown', function (e) { editCard(e); } );

form_element.submit( function (e) {
	createCards(e, form_element);
});

$('#togglePublic').change(function(e)
{
	var checked;
	if ($(this).is(':checked'))
		checked = 1;
	else
		checked = 0;
	console.log(checked);
	$.ajax({
		type: "GET",
		url: "/create/" + deck_id + "/" + checked + "/",
		success: function(data){
			//location.reload();
		}
	});
});

// Functions
// =============================================================
function createCards(e, form_element)
{
	e.preventDefault();
	
	var question = $('#spurning').val();
	var answer = $('#svar').val();

	var entry = {
		model 			: 'flashcards.card',
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
			console.log("Nöldur frá bakenda: " + error);
		}
	});
}

function Entry(id, deck_id)
{
	return {
		model 			: 'flashcards.card',
		pk				: id,
		fields 			: {
			deck		: deck_id,
			question 	: "",
			answer   	: "",
			active		: "",
			visible		: ""
		}
	};
}

function editCard(e, bypass) {

	bypass = bypass || false;

	// Bypass keycode checking, if we're using a
	// non-keydown event
	if(((e.which === enter_keycode) || bypass))
	{
		e.preventDefault();
		var target = $(e.target);

		var top_el = target.parent().parent();
		var id = top_el.attr('id');

		var question = "";
		var answer = "";
		var active = "";
		var visible = "";

		var entry = Entry(id, deck_id);

		if (target.attr('name') === "visible")
		{
			entry.fields[target.attr('name')] = target.is(':checked');
			console.log(entry.fields[target.attr('name')]);
		}
		else
		{
			entry.fields[target.attr('name')] = target.val();
		}

		var hiddenForm = $('#hidden');
		var hiddenFormField = $('#spjald');
		hiddenFormField.val(JSON.stringify([entry]));
		var data = hiddenForm.serialize();

		$.ajax({
		type: "POST",
		url: "/edit/",
		data: data,
		success: function(data) {
			console.log("Success editing card: " + data);
		},
		error: function(jqXHR, status, error){
			// Do not clear form if server does not 
			// save the card
			console.log("Nöldur frá bakenda: " + error);
		}
	});

	}
}

function deactivate(e) {
	e.preventDefault();

	var el = $(e.target).parent().parent();
	var id = el.attr('id');

	var hiddenForm = $('#hidden');
	var hiddenFormField = $('#spjald');
	hiddenFormField.val("");
	var data = hiddenForm.serialize();

	$.ajax({
		type: "POST",
		url: "/delete/" + id + "/",
		data: data,
		// TODO: Code for connecting correctly to backend
		success: function() {
			el.slideToggle(200, function () {this.remove();});
			console.log("Success deleting card: " + id);
		},
		error: function(jqXHR, status, error){
			// Do not clear form if server does not 
			// save the card
			console.log("Nöldur frá bakenda: " + error);
		}
	});
}

function clearForm(el) {
	$(el).find('input[type=text]').val("");
}

function prependAddedCard(data)
{
	var el = $('#tilbuin_spjold li.legend')

	var id = data[0].pk;
	var question = data[0].fields.question;
	var answer = data[0].fields.answer;

	var checked = ""
	if(data[0].fields.visible)
		checked = "checked";
	console.log(checked);

	var entry = {
		id : id,
		question : question,
		answer : answer,
		checked : checked
	};

	var template = $('#edit_card_view').html();
	var compiled = _.template(template);
	var html = compiled(entry);

	el.after(html);
}