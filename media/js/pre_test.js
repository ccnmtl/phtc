jQuery(document).ready(function () {
    var pre_test_input = jQuery('<input name="pre_test" value="true" type="hidden" />');
    var form = jQuery('form');
    jQuery('.pager').css({
        display: 'none'
    });
    form.prepend(pre_test_input);

function check_answers(questions){
	//console.log('fired')
	jQuery(questions).each(function(){
		var c = jQuery(this).find('input')
		jQuery(c).each(function(){
			if(jQuery(this).attr('checked') ){
				console.log(this)
			}else{
				console.log('nope')
			}	
		})
		if(jQuery(this).find('input').attr('checked') ){
			//console.log(jQuery(this).find('input').val() )
		}
	})
}//end check_answers()

jQuery('.casequestion li input').click(function(){
	var questions = jQuery('.casequestion');
	check_answers(questions);
})

});//end doc.ready
