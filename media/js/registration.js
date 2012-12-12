
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



