$('.flip').click(function(){
	$(this).find('.card').addClass('flipped').mouseleave(function(){
		$(this).removeClass('flipped');
	});
        return false;
});


$('.ans').click(function(){
    var id = $(this).attr('id');
    var card_id = id.match(/\d+$/)[0];
    var ans_value = id.substring(0, id.indexOf(card_id));

    $("#svar").val(ans_value);
    console.log($("#svar").val());
    $.ajax({
        type: "POST",
        url: "/" + card_id + "/",
        data: $("#hidden").serialize(),
        success: function() {
            console.log("Jibbí!");
        },
        error: function() {
            console.log("Jabbú!");
        }
    });
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