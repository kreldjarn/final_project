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

function showCards()
{
    var html = "";
    var template = $('#flip-card').html();
    var compiled = _.template(template);
    for(var i = 0; i < cards.length; ++i)
    {
        var c = cards[i];
        html += compiled({
            id: c.id,
            question: c.question,
            answer: c.answer
        });
    }

    $("section#cards").html(html);
}


// Færum þetta e-ð annað. Í raun til að rendera
// template-ið og spýta út í DOM ið eftir því hvernig
// röðin á kortunum eru í cards[] JS fylkinu
// S.s. til að update-a viewið fyrir læri-ham.
// Því við viljum geta shufflað/bætt aftast í random röð
// og svo framvegis, þegar líður á lærdóms-sessjón.
showCards();

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