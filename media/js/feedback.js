jQuery(document).ready(function() {
    jQuery('.casequestion form li').each(function() {
        jQuery(this).click(function() {
            //adding event listeners
            var casequestion = jQuery(this).parent().parent().parent().parent();
            var arr = jQuery(this).parent().children();
            var index = arr.index(this);
            var feedback = jQuery(casequestion).children('.case-feedback');
            var feedback_item = jQuery(casequestion)
                .children('.case-feedback').children()[index];

            jQuery(feedback).children().each(function() {
                jQuery(this).css('display','none');
            });
            jQuery(this).find('input:radio').attr('checked', true);

            jQuery(feedback_item).css({
                display: 'block'
            });

        });//end click
    });//end each
});// end doc.ready
