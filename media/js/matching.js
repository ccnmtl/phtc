/*
// This is the calculation and results display of the matching quizblock
*/
var shuffle_answers = [];
  
Array.prototype.shuffle = function () {
    var len = this.length;
    var i = len;
    while (i--) {
        var p = parseInt(Math.random() * len, 10);
        var t = this[i];
        this[i] = this[p];
        this[p] = t;
    }
};

jQuery('.table-matching').each(function () {
    shuffle_answers.push(this);
});

shuffle_answers.shuffle();

jQuery(shuffle_answers).each(function () {
    jQuery('#matching').append(this);
});

jQuery(document).ready(function ($) {
    //Globals
    var _user_answers = {};
    var _answer_key = window.correct_answers;

    //private
    var btn = $('input.btn.btn-primary');

    //add event listener
    btn.click(function () {
        $('.user-selection').each(function (i) {
            if ($(this).children().attr("checked")) {
                var answer_length = $('.answer-label').length;
                var answer = jQuery(jQuery('.answer-label')[(Math.floor(i / answer_length))]).html();
                _user_answers[answer] = $(this).children().val();
            }
        });
        window.user_answers = _user_answers;

        if (Object.keys(_answer_key).length !== Object.keys(_user_answers).length) {
            alert('Please answer each scenario item.');
            return;
        } else {
            alert('Your answers are in! \n Click ok to continue.');
            display_answer_comparison();
            return;
        }
    });//end .click


    function display_answer_comparison() {
        var btn = $('input.btn.btn-primary').clone();
        var _index = 0;

        $(btn).attr('value', 'try again');
        $('input.btn.btn-primary').replaceWith(btn);
        $(btn).click(function () { window.location.reload(); });

        $('#header-table td.td-ui').remove();
        $('#header-table tr')
            .append('<td class="td-answer-header">Your Answers</td> <td class="td-answer-header">Our Answers</td>');

        $('td.td-ui.user-selection').remove();
    
        for (var key in _answer_key) {
            if (_answer_key.hasOwnProperty(key)) {
                jQuery(jQuery('.table-matching')[_index]).children().children()
                    .append('<td class="td-answer-comparison">' +
                            _user_answers[jQuery(jQuery('.answer-label')[_index]).html()] +
                            '</td><td class="td-answer-comparison">' +
                            _answer_key[jQuery(jQuery('.answer-label')[_index]).html()] +
                            '</td>');
                _index += 1;
            }
        }
    
        $('#matching').append('<p class="explanation well">' + window.explanation.explanation + '</p>');
    }
});//end doc.ready



