$('.flip').click(function(){
	$(this).find('.card').addClass('flipped').mouseleave(function(){
		$(this).removeClass('flipped');
	});
        return false;
});


$('.card').click(function()
{
    var id = $(this).attr('id');
    var index;
    for(var i = 0; i < cards.length; i++) {
	if (cards[i].id === id) {
	    index = i;
	    break;
	}
    }
});