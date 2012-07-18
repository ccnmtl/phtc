/*
* undo all anchor tags  that are unititiated 
*/

var links = jQuery('.section_url');
var uninitiated = []

links.each(function(){
	var link = jQuery(this);
	var class_name = link.parent().next().children().attr('class')
	if(class_name == "uninitiated" ){
		uninitiated.push(link)
	}
})

jQuery(uninitiated).each(function(i){
	if(i === 0){
	}
	else if(jQuery(this).hasClass('module') ){

	}
	else if(jQuery(this).hasClass('part') ){

	}
	else{
		var link = jQuery(this);
		var linkSpan = '<span>'+ link.html() +'</span>'
		link.parent().append(linkSpan)
		link.remove()
	}
}) 

jQuery(document).ready(function($){
	$(".module-info-popover").popover({
    	offset: 10,
    	trigger:'manual'

    }).click(function(){
         $(this).popover('show')

    }).mouseleave(function(){
    	$(this).popover('hide')
    });

	$(".section-info-popover").popover({
    	offset: 10,
    	trigger:'manual'

    }).click(function(){
         $(this).popover('show')

    }).mouseleave(function(){
    	$(this).popover('hide')
    });
});//end doc.ready