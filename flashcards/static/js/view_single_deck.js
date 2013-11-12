$('.card').click( function(e){
    $(this).toggleClass('flip');
    e.stopDelegation();

        return false;
});


$('.ans').click(function(){
    var id = $(this).attr('id');
    var card_id = id.match(/\d+$/)[0];
    var ans_value = id.substring(0, id.indexOf(card_id));
    $.ajax({ url: "/" + card_id + "/" + ans_value + "/" });
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