var top_el = $("#cards");

var cards_3d_factor = 10;
var max_cards_drawn = 16;

function showCards()
{
    var html = '<div class="top">';
    var template = $('#flip-card').html();
    var compiled = _.template(template);

    for(var i = 0; i < cards.length; ++i)
    {
        if (i === max_cards_drawn) break;
        var c = cards[i];

        var dzoom = 1 - ((i / cards_3d_factor) * 0.2);
        if(dzoom < 0) dzoom = 0;

        var html_string = compiled({
            id: c.id,
            question: c.question,
            answer: c.answer,
            style: 'z-index: ' + (-1-i) +
            '; -webkit-transform: scale(' + dzoom + ')',
            extraClass : 'color' + Math.floor(i/2)
        });

        html += html_string;
        if(i === 0) html += '</div><div class="lower">'
    }

    html += '</div>';

    $("section#cards").html(html);
    console.log("Show cards");
}

$('#yfirlit').click(function(e)
{
    $.ajax({
        type: "GET",
        url: "/sessions/" + deck.id + "/",
        success: function(data) {
            console.log(data);
        }
    });
});

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
    updateCardView(ans_value);
    var card_ids = [];
    for (var i = 0; i < cards.length; i++)
    {
        card_ids.push(cards[i].id);
    }
    $("#remaining").val(JSON.stringify(card_ids));

    $.ajax({
        type: "POST",
        url: "/" + card_id + "/" + session_id + "/",
        data: $("#hidden").serialize(),
        success: function() {
            showCards();
        },
        error: function() {
        }
    });
});

function removeTopCard()
{
    if(cards.length > 0)
    {
        var card = cards[0];
        cards = cards.slice(1, cards.length);
        return card;
    }
    return false;
}

function updateCardView(ans_value)
{
    var card = removeTopCard();
    if(ans_value === "rangt")
    {
        cards.push(card);
    }
    //$('#results').append(result); 
}