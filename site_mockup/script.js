var flip_button = $("#flip");
var card = $(".card");

flip_button.on('click', function (e) {
	toggleClass(card, 'flip');
	console.log("typp");
})

function toggleClass (el, className) {
	if(!el.hasClass(className)) el.addClass(className);
	else el.removeClass(className);
}

// Stack cards in reverse order
$("ul.stack li").each(function (n) {
	$(this).find(".stack-card").css('z-index', -n);
});