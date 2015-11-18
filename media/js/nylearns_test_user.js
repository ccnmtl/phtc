(function(jQuery) {
    $(document).ready(function() {
        $('#id_password').focus(function() {
            var url_var_username = $('#id_username').val();
            $.post('/test_nylearns_username/', {username: url_var_username})
                .success(function(data, url_var_username) {
                    if (data == 'True') {
                        //username already exists
                        $('#nylearns-greeting')
                            .html('<p class="alert">Welcome Back!</p>');
                    } else {
                        var register = $('#nylearns-register-link').clone();
                        register
                            .attr('id', 'clone-nylearns-register-link')
                            .text('here');
                        $('#nylearns-greeting')
                            .html('<p class="alert">That Username does ' +
                                  'not exist. Please register </p>');
                        $('.alert').append(register).append('.');
                    }
                });
        });
    });
}($));
