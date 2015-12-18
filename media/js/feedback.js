jQuery(document).ready(function() {
    jQuery('.casequestion form button').each(function() {
        jQuery(this).click(function() {
            
            var casequestion = jQuery(this).parent().parent().parent();
            
            /* make array of answers */
            var arr = jQuery(this).parent().parent().find('li input:radio');
            
            /* find the selected answer */
            var index = arr.index(':checked');
            
            /* make array of responses to answers */
            var feedback = jQuery(casequestion).find('.case-feedback div.item-feedback.well');
            console.log("feedback");
            console.log(feedback);
            console.log("feedback[index]");
            console.log(feedback[index]);
            
            /* display the feedback that corresponds to the selected answer */
            var feedback_item = feedback[index];//jQuery(casequestion)
                //.children('.case-feedback .item-feedback').children()[index];
            console.log("feedback_item");
            console.log(feedback_item);

            jQuery(feedback).each(function() {
                jQuery(this).css('display','none');
            });
            //jQuery(this).find('input:radio').attr('checked', true);

            jQuery(feedback_item).css({
                display: 'block'
            });

        });//end click
    });//end each
});// end doc.ready
