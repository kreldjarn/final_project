// Global stuff here

// Stack cards in reverse order
$("ul.stack li").each(function (n) {
	$(this).find(".stack-card").css('z-index', -1-n);
});