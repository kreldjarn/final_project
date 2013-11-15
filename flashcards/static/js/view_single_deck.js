var top_el = $("#cards");

top_el.delegate(".card", "click", function (e) {
    $(this).toggleClass("flip");
});

top_el.delegate(".answer button", "click", function(e) {
    e.stopPropagation();

    var card_el = $(this).parent().parent().parent().parent();
    var card_id = card_el.attr('id');
    var ans_value = $(this).attr('data-id');

    $("#svar").val(ans_value);

    $.ajax({
        type: "POST",
        url: "/" + card_id + "/",
        data: $("#hidden").serialize(),
        success: function() {
            updateCardView(card_el, ans_value);
            console.log("Jibbí!");
        },
        error: function() {
            console.log("Jabbú!");
        }
    });
});

function updateCardView(card_el, ans_value)
{
    var cards_top_el = $("section#cards");
    card_el.remove();

    if(ans_value === "rangt")
    {
        card_el.find(".card").removeClass("flip");
        cards_top_el.append(card_el);
    }
}

function updateCardEvents()
{
    $('.card').click( function(e) {
        $(this).toggleClass('flip');
        e.stopPropagation();
        return false;
    });
}