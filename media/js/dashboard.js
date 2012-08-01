jQuery(document).ready(function(){ 
/*
** Initiate the bootstrap popup
*/
function add_bootstrap_popup(){
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
}

 /*
 ** Module/Part UI 
 */
 $('.show-module').click(function(){
 	var link = $(this).attr('rel')
 	var id = $(this).parent().attr('id')
    jQuery('.content').append('<div id="page-load"><h1>Loading...</h1</div>')
  	$.ajax({
		url: link,
		mod_id: id,
		type: "POST",
		data: { module: link, mod_id: id }
		}).done(function(data) {
            
			$('#return').empty().load('/dashboard_panel/ #part_id_'+ id, function(response, status, xhr){
				if(status == "success"){
					$('#return').children().children().css('display','block')
                    add_bootstrap_popup();
				}
            jQuery('#page-load').remove();
			})
		});
 	})//end click
});//end doc.ready