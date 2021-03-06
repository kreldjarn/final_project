// Global stuff here

// Stack cards in reverse order
$("#stacks ul.stack, #main ul.stack").each(function () {
	$(this).find("li").each(function (n) {
        $(this).find(".stack-card").addClass('color' + (2*n+1)).css('z-index', -1-n);
    });
});

function fixCardStackingOrder()
{
    $("#right ul.stack").each(function () {
        $(this).find("li").each(function (n) {
            $(this).find(".stack-card").css('z-index', -1-n);
        });
    });
}

fixCardStackingOrder();

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

