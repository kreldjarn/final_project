var top_el = $("#cards");

var cards_3d_factor = 10;
var max_cards_drawn = 16;
var currentColor = 'green';

// Underscore Templates

var single_card_template = $("script#single-card").html();
single_card_template = _.template(single_card_template);

var flip_card_template = $('#flip-card').html();
flip_card_template = _.template(flip_card_template);

// Render main stack

function showCards()
{
    var html = '<div class="top">';

    for(var i = 0; i < cards.length; ++i)
    {
        if (i === max_cards_drawn) break;
        var c = cards[i];

        var dzoom = 1 - ((i / cards_3d_factor) * 0.2);
        if(dzoom < 0) dzoom = 0;

        var html_string = flip_card_template({
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
}

$('#yfirlit').click(function(e)
{
    $.ajax({
        type: "GET",
        url: "/sessions/" + deck.id + "/",
        success: function(data) {
            data = $.parseJSON(data);
            console.log(data);
        }
    });
});

$('#shuffle').click(function(e)
{
    cards = shuffle(cards);
    showCards();
});

// Færum þetta e-ð annað. Í raun til að rendera
// template-ið og spýta út í DOM ið eftir því hvernig
// röðin á kortunum eru í cards[] JS fylkinu
// S.s. til að update-a viewið fyrir læri-ham.
// Því við viljum geta shufflað/bætt aftast í random röð
// og svo framvegis, þegar líður á lærdóms-sessjón.

// SEQUENTIAL LOGIC
// =======================================
cards = shuffle(cards);
showCards();

if (log)
{
    log = JSON.parse(log);
    for (var i in log)
    {
        var ans = 'red';
        if (log[i][1]) ans = 'green';
        var tmp = single_card_template({ color: ans });
        $('#right ul.stack').prepend(tmp);
        fixCardStackingOrder();
    }
}

// DELEGATIONS
// =======================================
top_el.delegate(".card", "click", function (e) {
    $(this).toggleClass("flip");
});

top_el.delegate(".answer button", "click", function(e) {
    e.stopPropagation();

    var card_el = $(this).parent().parent().parent().parent();
    var card_id = card_el.attr('id');
    var ans_value = $(this).attr('data-id');

    $("input#svar").val(ans_value);

    updateCardView(ans_value);

    var card_ids = [];
    for (var i = 0; i < cards.length; i++)
    {
        card_ids.push(cards[i].id);
    }

    $("input#remaining").val(JSON.stringify(card_ids));

    $.ajax({
        type: "POST",
        url: "/" + card_id + "/" + session_id + "/",
        data: $("#hidden").serialize(),
        success: function() {
            showCards();
            $("#right ul.stack").prepend(single_card_template({color: currentColor}));
            fixCardStackingOrder();
        },
        error: function() {
        }
    });
});

function shuffle(deck){
    for(var j, x, i = deck.length; i; j = Math.floor(Math.random() * i), x = deck[--i], deck[i] = deck[j], deck[j] = x);
    return deck;
};

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
    currentColor = "green";

    if(ans_value === "rangt")
    {
        cards.push(card);
        currentColor = "red";
    }
    
}