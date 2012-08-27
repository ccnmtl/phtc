var this_scenario = jQuery('.interactive-scenario').attr('id');
var this_scenario = this_scenario + 'form';

function generaterow() {
    for (i=0; i<2; i++) {
        for (j=0; j<4; j++) {
            if (j==0) {
                jQuery('form').append('<input name="notation" type="text" size="1" maxlength="2" id="r'+i+'c'+j+'" />');
            }
            else {
                jQuery('form').append('<input name="notation" type="text" size="1" maxlength="1" id="r'+i+'c'+j+'" />');
            }
        }
    jQuery('form').append('<br />');
    }
}

function create_designform() {
    jQuery('.interactive-scenario').append('<form/>');
    jQuery('.interactive-scenario form').attr('id', this_scenario);
    generaterow();
    jQuery('.interactive-scenario').append('<button id="checkanswer" type="submit" class="btn">Check answer</button>');
}

function check_input_validity() {
    jQuery('input').keyup(function() {
    var value = jQuery(this).val();
    if (value!="") {
        if (value=="0") { value = jQuery(this).val('o');}
        if (value=="-") { value = jQuery(this).val(' ');}
        if (value=="n" || value == "N") { value = jQuery(this).val('NR');}
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

function check_answer() {
    jQuery('#checkanswer').click(function() {
        var values = jQuery('input[ name="notation"]').map(function(){return $(this).val();}).get();
        alert(values);
    });
}

jQuery(document).ready(function(){

    create_designform();
    check_input_validity();
    check_answer();

    
});//end doc.ready


