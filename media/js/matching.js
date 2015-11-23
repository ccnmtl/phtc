/*
// This is the calculation and results display of the matching quizblock
*/
var shuffle_answers = [];

Array.prototype.shuffle = function() {
    var len = this.length;
    var i = len;
    while (i--) {
        var p = parseInt(Math.random() * len, 10);
        var t = this[i];
        this[i] = this[p];
        this[p] = t;
    }
};

jQuery('.table-matching').each(function() {
    shuffle_answers.push(this);
});

shuffle_answers.shuffle();

jQuery(shuffle_answers).each(function() {
    jQuery('#matching').append(this);
});

jQuery(document).ready(function($) {
    //Globals
    var _user_answers = {};
    var _answer_key = window.correct_answers;

    //private
    var btn = $('button.matching-quizblock');

    //clean string function
    function cleanup_string(str, kill_space) {
        var punctuationless = str.replace(
                /[\.,-\/?#!$%\^&\*;:{}=\-_`~()]/g, '');
        var spaceless;
        if (kill_space === true) {
            spaceless = punctuationless.replace(/\s/g, '');
        } else {
            spaceless = punctuationless;
        }
        var filter = spaceless.replace(/'/g,'');//take out the single quotes
        var filter1 = filter.replace(/\[/g,'');//replace [
        var filter2 = filter1.replace(/\]/g,'');//replace ]
        var clean_lower = filter2.toLowerCase();//to lowercase
        return clean_lower;
    }
    //add event listener
    btn.click(function() {
        $('.user-selection').each(function(i) {
            if ($(this).children().attr('checked')) {
                var answer_length = $('.answer-label').length;
                var answer = cleanup_string(
                    jQuery(jQuery(
                        '.answer-label')[(Math.floor(i / answer_length))])
                        .html(), true);
                _user_answers[answer] = cleanup_string(
                    $(this).children().val(), false);
            }
        });
        window.user_answers = _user_answers;

        if (Object.keys(_answer_key).length !== Object.keys(_user_answers)
            .length) {
            alert('Please answer each scenario item.');
            return;
        } else {
            alert('Your answers are in! \n Click ok to continue.');
            display_answer_comparison();
            return;
        }
    }); //end .click

    function display_answer_comparison() {
        var btn = $('button.matching-quizblock').clone();
        var _index = 0;

        $(btn).html('try again');// attr('', 'try again');
        $('button.matching-quizblock').replaceWith(btn);
        $(btn).click(function() {
            window.location.reload();
        });
        $('#header-table td.td-ui').remove();
        $('#header-table tr')
            .append('<td class="td-answer-header">Your ' +
                    'Answers</td> <td class="td-answer-' +
                    'header">Our Answers</td>');
        $('td.td-ui.user-selection').remove();

        for (var key in _answer_key) {
            if (_answer_key.hasOwnProperty(key)) {
                var label =  cleanup_string(
                    jQuery(jQuery('.answer-label')[_index]).html(), true);
                jQuery(jQuery('.table-matching')[_index]).children().children()
                    .append('<td class="td-answer-comparison">' +
                            _user_answers[label] +
                            '</td><td class="td-answer-comparison">' +
                            _answer_key[label] +
                            '</td>');
                _index += 1;
            }
        }

        $('#matching').append('<p class="explanation well">' +
                              window.explanation.explanation + '</p>');
    }
});//end doc.ready
