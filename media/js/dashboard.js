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
 	var child = $('#'+id).children('.part')
 	var ch_clone = $(child).clone()
 	console.log(id)
 	ch_clone.css('display','block')
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
			})
		});
 	})//end click
});//end doc.ready