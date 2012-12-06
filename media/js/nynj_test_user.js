(function(jQuery){
	$(document).ready(function(){
		$('#id_username').focus()
		$('#id_username').blur(function(){
			url_var_username = $('#id_username').val()
			$.post('/test_nynj_username/',{ username: url_var_username}
			)
			.success(function(data, url_var_username){
				if (data == 'True'){//username already exists
					$('#nynj-greeting').html('<p class="alert">Welcome Back!</p>')
				}else{
					var register = $('#nynj-register-link').clone().text('here')
					$('#nynj-greeting').html('<p class="alert">That Username does not exist. Please register </p>')
					$('.alert').append(register).append('.')
				}
			});
		})
	})
}($))