jQuery(document).ready(function() {

    var scenario;
    var colNum = 0;

    var cellTotal = 0;
    var scenario2_answer = ' ' + 'O' + 'X' + 'O' + ' ' +
        ' ' + ' ' + ' ';
    var scenario3_answer = 'R' + 'O' + 'X' + 'O' + 'R' +
        'O' + ' ' + 'O';
    var finaldesign_answer = 'NR' + 'O' + 'X' + 'O' + 'O' +
        'NR' + 'O' + ' ' + 'O' + 'O';
    var correctAnswer = '';

    function initScenario() {
        scenario = jQuery('.interactive-scenario').attr('id');
        if (scenario === 'scenario2') {
            colNum = 4;
            cellTotal = 8;
            correctAnswer = scenario2_answer;
        }
        if (scenario === 'scenario3') {
            colNum = 4;
            cellTotal = 8;
            correctAnswer = scenario3_answer;
        }
        if (scenario === 'finaldesign') {
            colNum = 5;
            cellTotal = 10;
            correctAnswer = finaldesign_answer;
        }
    }

    function generateSelector() {
        var notationValue = ['NR', 'R', 'X', 'O', '&nbsp;'];
        var divCell = [];
        jQuery('.interactive-scenario')
            .append('<div class="notation_select" id="notation_selections">');
        for (var i = 0; i < notationValue.length; i++) {
            divCell[i] = '<div class="notation_option btn btn-primary">' +
                notationValue[i] + '</div>';
            jQuery('.notation_select').append(divCell[i]);
        }
    }

    function generateGrid() {
        jQuery('.interactive-scenario')
            .append('<div class="notation_gridbox">');
        for (var i = 0; i < 2; i++) {
            jQuery('.notation_gridbox')
                .append('<div class="notation_row">');
        }
        for (var j = 0; j < colNum; j++) {
            jQuery('.notation_row')
                .append('<div class="notation_field" id="r' +
                        i + 'c' + j + '" />');
        }
        jQuery('.interactive-scenario')
            .append('<button id="checkanswer" type="submit" ' +
                    'class="btn">Check answer</button>');
    }

    function show_notation_select() {
        var srcElement;
        jQuery(document).click(function() {
            jQuery('.notation_select').removeClass('visible');
            jQuery('.notation_field').removeClass('active');
            jQuery('.notation_gridbox').removeClass('nomargin_gridbox');
        });

        jQuery('.notation_field').click(function(evt) {
            jQuery('.notation_field').removeClass('active');
            jQuery('.notation_select').addClass('visible');
            jQuery('.notation_gridbox').addClass('nomargin_gridbox');
            evt.stopPropagation();
            srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).addClass('active');
        });

        jQuery('.notation_option').click(function(evt) {
            evt.stopPropagation();
            var notation_value = jQuery(this).html();
            jQuery(srcElement).html(notation_value);
            jQuery('.notation_select').removeClass('visible');
            jQuery('.notation_field').removeClass('active');
            jQuery('.notation_gridbox').removeClass('nomargin_gridbox');
            jQuery(srcElement).addClass('hasvalue');
        });
    }

    function resetFeedback() {
        jQuery('.notation_feedback').removeClass('visible');
        jQuery('.no_entry').removeClass('visible');
        jQuery('.notation_correct').removeClass('visible');
        jQuery('.notation_incorrect').removeClass('visible');
        jQuery('.notation_undetermined').removeClass('visible');
        jQuery('.notation_answerkey').removeClass('visible');
    }

    function check_answer() {
        jQuery('#checkanswer').click(function() {
            var useranswer = '';
            var blank_answer = 0;
            jQuery('.notation_field').each(function(index) {
                if (jQuery(this).html() === '') {
                    blank_answer++;
                }
                if (jQuery(this).html() === '&nbsp;') {
                    jQuery(this).html(' ');
                }
                useranswer += (jQuery(this).html());
            });

            if (blank_answer === cellTotal) {
                resetFeedback();
                jQuery('.notation_feedback').addClass('visible');
                jQuery('.no_entry').addClass('visible');
            } else if ((blank_answer < cellTotal) && (blank_answer !== 0)) {
                resetFeedback();
                jQuery('.notation_feedback').addClass('visible');
                jQuery('.notation_undetermined').addClass('visible');
            } else {
                if (useranswer === correctAnswer) {
                    resetFeedback();
                    jQuery('.notation_feedback').addClass('visible');
                    jQuery('.notation_correct').addClass('visible');
                } else {
                    resetFeedback();
                    jQuery('.notation_feedback').addClass('visible');
                    jQuery('.notation_incorrect').addClass('visible');
                }
            }
        });
    }

    function showAnswerkey() {
        jQuery('#show_answerkey_grid').click(function() {
            jQuery('.notation_answerkey').addClass('visible');
        });
    }

    initScenario();
    generateSelector();
    generateGrid();
    show_notation_select();
    check_answer();
    showAnswerkey();
});

