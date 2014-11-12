jQuery(document).ready(function(){

	var question_number = 4; //enter the number of the question you would like to augment
	var question = jQuery( jQuery('.special-question').children('.cases')[question_number -1] );
	// set the answers as available src string variables
	var a1 = 'Mod2PPTQ4A.jpg';
	var a2 = 'Mod2PPTQ4B.jpg';
	var a3 = 'Mod2PPTQ4C.jpg';
	var a4 = 'Mod2PPTQ4D.jpg'; 
	var answer_array = [a1,a2,a3,a4];
	question.children('.casecontent').children('.casequestion').children('.answerchoices').children('li').children('input').each(function(i){
		var img = new Image();
		jQuery(img).attr('src', '/media/img/' + answer_array[i]);
		jQuery(this).after(img);
	});
});
