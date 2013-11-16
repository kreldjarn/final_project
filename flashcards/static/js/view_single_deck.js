var top_el = $("#cards");

function showCards()
{
    var html = '<div class="top">';
    var template = $('#flip-card').html();
    var compiled = _.template(template);
    for(var i = 0; i < cards.length; ++i)
    {
        var c = cards[i];
        var zind = i === 0 ? 'inherit' : -1-i;

        var html_string = compiled({
            id: c.id,
            question: c.question,
            answer: c.answer,
            zind: zind
        });

        html += html_string;
        if(i === 0) html += '</div>';
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

///////////////////////////////////////////////////////

function updateCardView(card_el, ans_value)
{
    var cards_top_el = $("section#cards");
    console.log(card_el.id);


    if(ans_value === "rangt")
    {
        card_el.find(".card").removeClass("flip");
        cards_top_el.append(card_el);
    }

    showCards();
}