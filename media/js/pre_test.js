jQuery(document).ready(function () {
	var btn = jQuery('.btn.btn-primary');
	var btn_hold = jQuery('<div class="btn btn-secondary style="background:#333 important!;">Submit*</div>') 

    var pre_test_input = jQuery('<input name="pre_test" value="true" type="hidden" />');
    var form = jQuery('form');

    btn.css('display','none');
    jQuery('#content').append(btn_hold);
    jQuery('.pager').css({
        display: 'none'
    });

    form.prepend(pre_test_input);

function check_answers(questions){
	//console.log('fired)
	var num_of_questions = questions.length;
	var num_of_answers = 0;
	jQuery(questions).each(function(){
		var c = jQuery(this).find('input')
		jQuery(c).each(function(){
			if(jQuery(this).attr('checked') ){
				console.log(this);
				num_of_answers += 1;
			}else{
				//console.log('nope')
			}	
		})
		if(jQuery(this).find('input').attr('checked') ){
			//console.log(jQuery(this).find('input').val() )
		}
	})//end .each
	if(num_of_answers === num_of_questions){
		btn_hold.css('display','none');
		btn.css('display','block');
	};
	console.log("_________");
}//end check_answers()

jQuery('.casequestion li input').click(function(){
	var questions = jQuery('.casequestion');
	check_answers(questions);
})

});//end doc.ready
