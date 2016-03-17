function CheckboxActivity($, context) {
    Object.prototype.keys = function() {
        var keys = [];
        for (var i in this) {
            if (this.hasOwnProperty(i)) {
                keys.push(i);
            }
        }
        return keys;
    };

    // globals
    var that = this;
    // do this so the context of "this" (instance of the
    //CheckboxActivity) can be refferred to when out of scope
    this.context = context;
    this.attrs = ['blank',
                  'Leads researcher to fixate on details',
                  'Possible misinterpretations due to cultural differences',
                  'Requires technical training',
                  'Depends on cooperation of key individuals',
                  'Readily open to ethical dilemmas',
                  'Difficult to replicate',
                 ];

    this.objects = [// this is the object with a matches array
        // assign the key of the object to the correct
        // match in the attrs array
        {'Participant Observation': [1,2,0,4,5,6]},
        {'Observation': [1,2,0,0,5,6]},
        {'In-depth Interviews': [0,2,0,4,5,6]},
        {'Focus Groups': [0,2,3,0,0,6]},
        {'Document & AV Analysis': [1,2,0,4,5,6]}
    ];

    this.columnTitle = 'Method of Collection';

    this.rowTitle = 'Challenges';

    this.submitButton = $('<button type="button" class="' +
                          'submit-button btn btn-secondary">Submit</button>');
    this.clearButton = $('<button type="button" class="' +
                         'clear-button btn btn-secondary">' +
                         'Clear Answers</button>');
    this.createMatches = function(attrs, objects) {
        window.objs = objects;
        //this function will create the objects();
        // with the correct attrsibutes
        for (var i = 0; i < objects.length; i++) {
            var obj = objects[i];
            var key = obj.keys();
            var matchString = [];
            for (var j = 0; j < obj[key].length; j++) {
                var attrsString = attrs[obj[key][j]];
                matchString.push(attrsString);
            }
            objects[i].matches = matchString;
        }

    };

    this.createGrid = function(activity) {
        var table = $('<table/>');
        var objs = $(activity.objects);
        var attrs = $(activity.attrs);
        var wrapper = $('<div class="checkbox-wrapper cases"/>');
        attrs.each(function(i) {
            var tr = $('<tr class="activity-row"></tr>');
            if (i > 0) {
                //account for added 'blank' attribute
                objs.each(function(j) {
                    var obj = objs[j];
                    var classMatch = 'interactive match-' +
                        obj[obj.keys()[0]][i - 1];
                    if (j === 0) {
                        tr.append('<td class="row-header">' + attrs[i] +
                                  '</td>');
                    }
                    tr.append('<td class="' + classMatch + '"></td>');
                });
                table.append(tr);
            } else {
                var columnRow = $('<tr class="column-row"/>');
                //insert a spacer column to account for the row headers
                columnRow.append('<td class="column-spacer">&nbsp;</td>');
                objs.each(function(k) {
                    var obj = objs[k];
                    var columnHeader = obj.keys()[0];
                    columnRow.append('<td class="column-header">' +
                                     columnHeader + '</th>');
                });
                table.append(columnRow);
            }//end if
        }); //end .each

        wrapper.append('<div id="column-title">' + this.columnTitle + '</div>');
        wrapper.append('<div id="row-title">' +
                       this.createRowTitle(this.rowTitle) + '</div>');
        this.submitButton.click(function() {
            var clearBtn = $('.clear-button');
            that.getAnswers();
            that.showAnswers();
            that.showAnswerKey();
            $(this).remove();
            $('.interactive').off();
            clearBtn.text('Retry');
            clearBtn.off();
            clearBtn.click(function() {
                location.reload();
            });
            that.customEmbed();
        });

        this.clearButton.click(function() {
            that.clearAnswers();
        });
        wrapper.append(table);
        this.context.append(wrapper);
        this.context.append(this.submitButton);
        this.context.append(this.clearButton);
        $('.interactive').click(function() {
            if ($(this).children().length > 0) {
                $(this).children().each(function() {
                    if ($(this).attr('class') === 'user-x') {
                        $(this).parent().empty();
                    }
                });
            } else {
                $(this).toggleClass('marked')
                    .append('<span class="user-x">X</span>');
            }
        });
        that.customEmbed('hide');
    };// end createGrid()

    this.createRowTitle = function(rowTitle) {
        var formattedRowTitle = '';
        for (var l in rowTitle) {
            if (l.length === 1) {
                formattedRowTitle += rowTitle[l] + '<br/>';
            }
        }
        return formattedRowTitle;
    };

    this.getAnswers = function() {
        var answerArr = [];
        $('.activity-row').each(function() {
            var row = $('.interactive', $(this));
            answerArr.push(row);
        });
        var sortedAnswers = this.getColumnAnswers(answerArr);
        window.answers = sortedAnswers;
        return sortedAnswers;
    };

    this.getColumnAnswers = function(answerArr) {
        // create array of objects with column as key
        // then compare to original objects object
        var returnedColumnSets = [];
        var columnCnt = answerArr[0].length;
        for (var i = 0; i < columnCnt; i++) {
            var tmpArr = [];
            for (var j = 0; j < answerArr.length; j++) {
                tmpArr.push($($($(answerArr)[j])[i]));
            }
            var column = {};
            var columnName = this.objects[i].keys()[0];
            column[columnName] = tmpArr;
            returnedColumnSets.push(column);
        }//end for
        return returnedColumnSets;
    };

    this.showAnswers = function() {
        $('.interactive').each(function() {
            var className = $(this).attr('class');
            var pattrn = /match-0/i;
            if (className.match(pattrn)) {
            } else {
                $(this).append('<span class="answr-x">X</span>');
                if ($(this).children().length > 0) {
                    if ($(this).children().length > 1) {
                        $(this).find('.answr-x').remove();
                    }
                    $(this).children().each(function() {

                        if ($(this).attr('class') !== 'answr-x') {
                            $(this).parent()
                                .append('<span class="answr-x">X</span>');
                        }
                    });
                }
            }
        });
    };

    this.clearAnswers = function() {
        $('.interactive').each(function() {
            $(this).html('');
        });
        $('.answer-key-wrapper').remove();
    };

    this.showAnswerKey = function() {
        var userAnswer = '<div>Your Answer:<span class=' +
            '"user-x"> X</span></div>';
        var correctAnswer = '<div>Correct Answer:<span ' +
            'class="answr-x"> X</span></div>';
        var html = $('<div class="answer-key-wrapper"><div ' +
                     'class="user-answers">' +
                     userAnswer + '</div><div class="activity-answers">' +
                     correctAnswer + '</div></div>');

        $('.checkbox-wrapper').append(html);
    };

    // A custom function that allows for stuff that is specific to the
    // site that the activity is embedded into.
    this.customEmbed = function(command) {
        if (command === 'hide') {
            $('.pager').css({
                display: 'none'
            });
        } else {
            $('.pager').css({
                display: 'block'
            });
        }
    };

    //initialize the activity
    this.createMatches(this.attrs, this.objects);
}
$(document).ready(function() {
    // create new Checkbox - the arguments are jQuery and
    // where the activity should be places on the page

    var activity = new CheckboxActivity($, $('#content'));
    activity.createGrid(activity);
});

