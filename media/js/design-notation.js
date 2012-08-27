jQuery(document).ready(function(){

    var this_scenario = jQuery('.interactive-scenario').attr('id');
    var this_scenario = this_scenario + 'form';
    
    function generaterow() {
        for (i=0; i<4; i++) {
            jQuery('form').append('<input type="text" size="1" maxlength="1" />');
        }
    }

    function create_designform() {
        jQuery('.interactive-scenario').append('<form/>');
        jQuery('.interactive-scenario form').attr('id', this_scenario);
        generaterow();
    }
    
    
    
    create_designform();
    
});//end doc.ready
