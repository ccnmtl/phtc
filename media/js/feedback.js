jQuery(document).ready(function() {
    jQuery('.casequestion form button').each(function() {
        jQuery(this).click(function() {
            
            var casequestion = jQuery(this).parent().parent().parent();
            console.log(casequestion);
            
            /* make array of answers */
            var arr = jQuery(this).parent().parent().find('li input:radio'); // took off a .parent()
            //console.log('arr');
            //console.log(arr);
            //console.log('arr.length()');
            //console.log(arr.length);
            
            /* find the selected answer */
            /* This works */
            var radios = arr.index(':checked');
            console.log('radios');
            console.log(radios);
            // jQuery('input:radio:checked:checked');
            //var radios = arr.index('li input:radio');
            //console.log('radios');
            //console.log(radios);
            
            //var sel_radio = radios.find(':checked');
            
            //var sel_radio = arr.index('input:radio'); // jQuery(arr).find('input:radio').attr('checked', true);
            //console.log('sel_radio');
            //console.log(sel_radio);
            
            var index = radios.index(sel_radio);
            console.log(index);
            
            //var index = arr.index(this);
            //console.log(index);
            
            /* make array of answers */
            var feedback = jQuery(casequestion).children('.case-feedback');
            //console.log("feedback");
            //console.log(feedback);
            
            /* make array of answers */
            var feedback_item = jQuery(casequestion)
                .children('.case-feedback').children()[index];
            //console.log("feedback_item");
            //console.log(feedback_item);

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
