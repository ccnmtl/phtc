jQuery(document).ready(function(){

	var submit_btn = jQuery('.btn-primary');
	var submit_clone = jQuery('<input type="button" value="Submit" class="btn">');

	// hide submit_btn and appned clone
	submit_btn.css('display','none');
	submit_btn.parent().append(submit_clone);
	submit_clone.click(function(){
		alert('Please answer all questions.');
	})

	jQuery('.reading-exercise').blur(function(){
		var num_answers = jQuery('.reading-exercise').length;
		var answered = [];
		jQuery('.reading-exercise').each(function(){
			if(jQuery(this).val() != ""){
				answered.push(true);
				check_answer();
			}
			
			function check_answer(){ 
				if (answered.length == num_answers){
					submit_clone.remove();
					submit_btn.css('display','block');
				}
			}
		})//end .each()

	})//end .blur()

})// end doc.ready