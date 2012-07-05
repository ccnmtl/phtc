/*
// This is the calculation and results display of the matching quizblock
*/

jQuery(document).ready(function($){
  //Globals
	var _user_answers = {};
	var _answer_key = window.correct_answers;
  //private
	var btn = $('input.btn.btn-primary');

  //add event listener
	btn.click(function(){
		$('.user-selection').each(function(i){
			if($(this).children().attr("checked") ){
				var answer_length = $('.answer-label').length;
				var answer = Math.floor(i/answer_length);
				_user_answers[answer] = $(this).children().val() ;
			}
		});
		window.user_answers = _user_answers;

		if(Object.keys(_answer_key).length != Object.keys(_user_answers).length){
			alert('Please answer each scenario item.');
			return;

		}else{
			alert('Your answers are in! \n Click ok to continue.');
			display_answer_comparison();
			return;
		}
  });//end .click


	function display_answer_comparison(){
		var btn = $('input.btn.btn-primary').clone();
		$(btn).attr('value','try again');
		$('input.btn.btn-primary').replaceWith(btn);
		$(btn).click(function(){ window.location.reload(); });

		$('#header-table td.td-ui').remove();
		$('#header-table tr')
			.append('<td class="td-answer-header">Your Answers</td> <td class="td-answer-header">Our Answers</td>');

		$('td.td-ui.user-selection').remove();
		$('.table-matching').each(function(i){
			$(this).children().children()
        .append('<td class="td-answer-comparison">' + _user_answers[i] + '</td><td class="td-answer-comparison">'+ _answer_key[i] +'</td>');
		});//end .each
		$('#matching').append('<p class="explanation well">' + window.explanation.explanation + '</p>');
	}
});//end doc.ready



