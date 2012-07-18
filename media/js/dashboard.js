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
	if(jQuery(this).hasClass('module') ){
		//do not replace link
	}
	else if(jQuery(this).hasClass('part') ){
		//do not replace link
	}
	else if(typeof next_section_status == "boolean"){
		if(next_section_status == true){
			//do not replace link
			next_section_status = false;
		}
		else{
			replaceLink(jQuery(this) );	
		}
	}
	else{
		replaceLink(jQuery(this) );	
	}
	function replaceLink(link){
		//replace link
		var linkSpan = '<span>'+ link.html() +'</span>'
		link.parent().append(linkSpan)
		link.remove()
	}
}) 

jQuery(document).ready(function(){ 

/*
* Initiate the bootstrap popup
*/
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