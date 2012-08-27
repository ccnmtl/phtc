jQuery(document).ready(function(){

    function create_designform() {
        var this_scenario = jQuery('.interactive-scenario').attr('id');
        jQuery('.interactive-scenario').append('<form/>');
        jQuery('.interactive-scenario form').attr('id', this_scenario);   
    }
    
    create_designform();
    
});//end doc.ready
