var flip_button = $("button#flip");
var card = $(".card");

flip_button.on('click', function (e) {
	toggleClass(card, 'flip');
	console.log("typp");
})

function toggleClass (el, className) {
	if(!el.hasClass(className)) el.addClass(className);
	else el.removeClass(className);
}