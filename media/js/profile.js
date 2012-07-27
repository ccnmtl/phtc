jQuery('#id_password1')
    .parent()
    .append('<span>Leave Blank to keep the same password</span>');
jQuery('#id_password2')
    .parent()
    .append('<span>Leave Blank to keep the same password</span>');

jQuery('input.btn').click(function () {
    var valid = 0;
    var password_valid = 0;
    var p1 = jQuery('#id_password1').val();
    var p2 = jQuery('#id_password2').val();
    jQuery('.help-inline').remove();
    jQuery('.controls').each(function (i) {
        if (jQuery(this).children().attr('id') === 'id_password1' ||
            jQuery(this).children().attr('id') === 'id_password2') {
            //skip password validation
        } else {
            jQuery(this).parent().removeClass('error');
            if (jQuery(this).children().val() === 'Please Select' ||
                jQuery(this).children().val() === '') {
                jQuery(jQuery('.controls')[i])
                    .append('<span class="help-inline">this field is required</span>')
                    .parent().addClass('error');
                valid += 1;
            }
        }  //end if password
    });  //end each

    //password validation
    if (p1 === '' && p2 === '') {
        password_valid  = 0;
    } else if (p1 === p2) {
        password_valid = 0;
    } else {
        jQuery(".alert").show();
        password_valid += 1;
    }
    if (valid === 0 && password_valid === 0) {
        jQuery('#user_profile').submit();
    }
});//end .click

//close the alert
jQuery('button.close-alert').click(function () {
    jQuery(this).parent().css('display', 'none');
});

//catch if the profile has been saved
jQuery(document).ready(function () {
    var loc = document.location.href.split('profile').pop();
    if (typeof(loc) === 'string' && loc === "/?saved=true/") {
        jQuery('#myModal').modal('toggle');
    }
});
