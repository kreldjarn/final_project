// Global stuff here

// Stack cards in reverse order
$("ul.stack").each(function () {
	$(this).find("li").each(function (n) {
        $(this).find(".stack-card").addClass('color' + n).css('z-index', -1-n);
    });
});

// Remove card object from JS array, with given ID
function removeCardWithId(id)
{
    for(var i = 0; i < cards.length; ++i)
    {
        // Ok, ég þurfti að skrifa sequential search …
        if(cards[i].id === id)
        {
            cards = cards.slice(i, 1);
            return i;
        }
    }
    return false;
}

