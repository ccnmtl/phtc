jQuery(document).ready(function () {
    var btn = jQuery('.btn.btn-primary');
    var btn_hold = jQuery('<div class="btn btn-secondary" style="margin-top:-10px;">Submit*</div>');
    var form = jQuery('form');

    function check_answers(questions) {
        var num_of_questions = questions.length;
        var num_of_answers = 0;
        jQuery(questions).each(function () {
            var c = jQuery(this).find('input');
            jQuery(c).each(function () {
                if (jQuery(this).attr('checked')) {
                    num_of_answers += 1;
                }
            });
        });//end .each
        if (num_of_answers === num_of_questions) {
            btn_hold.css('display', 'none');
            btn.css('display', 'block');
        }
    }//end check_answers()

    function init() {
        btn.css('display', 'none');
        btn_hold.click(function () {
            alert('Please answer all the required questions.');
        });
        jQuery('#content').append(btn_hold);
        jQuery('.pager').css('display', 'none');
        jQuery('.casequestion li input').click(function () {
            var questions = jQuery('.casequestion').children('ol').parent();
            check_answers(questions);
        });
    }//end init

    init();
});//end doc.ready
