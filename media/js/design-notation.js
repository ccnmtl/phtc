jQuery(document).ready(function(){

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
    
    create_designform();

    jQuery('input').keyup(function() {
    var value = jQuery(this).val();
    if (value=="0") { value = 'o'; jQuery(this).val('o');}
    if (value!="") {jQuery(this).addClass('hasvalue');}
    else if (jQuery(this).attr('class')) {jQuery(this).removeClass();}
    });
    
    
    
});//end doc.ready
