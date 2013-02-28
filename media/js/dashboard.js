jQuery(document).ready(function(){ 
    /*
    ** Move the video modules into the video area
    */    

    function move_video_modules(){
        if($('span.hide.video').length > 0){
            $('#modules').append('<h2 style="margin-top:40px">Videos, Webinars, and Lectures</h2>');
        }
        $('span.hide.video').each(function(){
            var clone = $(this).parent().clone();
            $(this).parent().remove();
            $('#modules').append(clone);

        })
    }
    move_video_modules()

    /*
    ** Initiate the bootstrap popup
    */
    function add_bootstrap_popup(){
        $(".module-info-popover").popover({
            offset: 10,
            trigger:'manual'

        }).click(function(){
            $(this).popover('show');

        }).mouseleave(function(){
            $(this).popover('hide');
        });

        $(".section-info-popover").popover({
            offset: 10,
            trigger:'manual'

        }).click(function(){
            $(this).popover('show');

        }).mouseleave(function(){
            $(this).popover('hide');
        });
    }
    add_bootstrap_popup();

    /*
    ** Module/Part UI 
    */
    $('.show-module').click(function(){
        $('.show-module').parent().removeClass('active')
        $(this).parent().toggleClass('active')
        var link = $(this).attr('rel');
        var id = $(this).parent().attr('id');
        jQuery('.content').append('<div id="page-load"><h1>Loading...</h1</div>');
        $.ajax({
            url: link,
            mod_id: id,
            type: "POST",
            data: { module: link, mod_id: id }
        }).done(function(data) {
            
            $('#return').empty().load('/dashboard_panel/ #part_id_'+ id, function(response, status, xhr){
                if(status == "success"){
                    $('#return').children().children().css('display','block');
                    add_bootstrap_popup();
                }
                jQuery('#page-load').remove();
            });
        });
    });//end click

    // NYNJ -> is the course available?
    if (PHTC.getUrlVars()['course_not_available'] == "true"){
        jQuery('#myModal').modal('toggle');
    }

});//end doc.ready
