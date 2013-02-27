
	var other_employment_location = jQuery('.employment-location-input').parent().parent();
	var clone_employment_location = other_employment_location.clone();
	var other_position = jQuery('.position-category-input').parent().parent();
	var clone_position = other_position.clone();

	
	if(other_employment_location.val() !== "Other"){
		other_employment_location.remove();
	}

	if (other_position.val() !== "Other"){
		other_position.remove();
	}
	
	jQuery('.employment-location').change(function(){
		if (jQuery(this).val() === "Other"){
			jQuery(this).after(clone_employment_location);
		}else{
			jQuery(this).next().remove();
		}
	});

	jQuery('.position-category').change(function(){
		if (jQuery(this).val() === "Other"){
			jQuery(this).after(clone_position);
		}else{
			jQuery(this).next().remove();
		}
	});


// set username to form if exists in URL
/*
jQuery(document).ready(function(){
	var Url_vars = PHTC.getUrlVars();
	console.log(Url_vars);
	if(Url_vars['username']){
		//we know this is a nynj user from the URL parmas
		jQuery('#id_is_nynj').val('True')
		// set the form's username to try the original nynj username if not already filled out
		var usrnm_val = jQuery('#id_username').attr('value')
		if (usrnm_val == '' ){
			jQuery('#id_username').val(Url_vars['username'])
		}
		// set the hidden field's value to record original nynj usernamein userprofile
		jQuery('#id_nynj_username').val(Url_vars['username'])
	}
	if(Url_vars['user_id']){
		jQuery('#id_nynj_user_id').val(Url_vars['user_id'])
	}
	if(Url_vars['course']){
		jQuery('#id_nynj_course_init').val(Url_vars['course'])
	}

})
*/