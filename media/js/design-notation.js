var scenario = jQuery('.interactive-scenario').attr('id');
var this_scenario = scenario + 'form';

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
    var scenario2_answer = ' '+'O'+'X'+'O'+' '+' '+' '+' ';
    var scenario3_answer = 'R'+'O'+'X'+'O'+'R'+'O'+' '+'O';
    jQuery('#checkanswer').click(function() {
        // get the values of the input
        var useranswer = "";
        jQuery('.hasvalue').each(function(){
            useranswer+=(jQuery(this).val());            
        });
        useranswer = useranswer.toUpperCase();
        
        if (useranswer==scenario2_answer) {alert('correct');}
        else {alert('my cat is smarter than you are');}
        
      //  console.log(useranswer);
      //  var useranswer = [];
     //   jQuery('.hasvalue').each(function(){
     //       useranswer.push(jQuery(this).val());            
     //   });
     //   console.log(useranswer);
     // check for null values, if null (not blank or -), return error saying user needs to completer everything
     // transform to lower case or uppercase, convert 0s if necessary
     // compare to the correct answer
     // return some kind of answer
     // 
     // 
    });
}
jQuery(document).ready(function(){

    create_designform();
    check_input_validity();
    check_answer();

    
});//end doc.ready


