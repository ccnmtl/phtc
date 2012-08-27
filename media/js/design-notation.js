    var this_scenario = jQuery('.interactive-scenario').attr('id');
    var this_scenario = this_scenario + 'form';
    
    function generaterow() {
        for (i=0; i<2; i++) {
            for (j=0; j<4; j++) {
                jQuery('form').append('<input type="text" size="1" maxlength="1" id="r'+i+'c'+j+'" />');
            }
        jQuery('form').append('<br />');
        }
    }

    function create_designform() {
        jQuery('.interactive-scenario').append('<form/>');
        jQuery('.interactive-scenario form').attr('id', this_scenario);
        generaterow();
    }
    
    function check_input_validity() {
        jQuery('input').keyup(function() {
        var value = jQuery(this).val();
        if (value!="") {
            if (value=="0") { value = jQuery(this).val('o');}
            if (value=="-") { value = jQuery(this).val(' ');}
            value = jQuery(this).val();
            value = value.toUpperCase();
            if (value=='O' || value=='X' || value=='R' || value=='NR' || value==' ') {
             jQuery(this).addClass('hasvalue');
           }
           else {
               alert('You have entered an illegal value "' + value +'". Please read the instructions and try again.');
           }
        }
        else if (jQuery(this).attr('class')) {jQuery(this).removeClass();}
        });
     }

jQuery(document).ready(function(){

    create_designform();
    check_input_validity();
    
});//end doc.ready
