jQuery(document).ready(function () {
    var pre_test_input = jQuery('<input name="post_test" value="true" type="hidden" />');
    var form = jQuery('form');
    jQuery('.pager').css({
        display: 'none'
    });
    form.prepend(pre_test_input);
});
