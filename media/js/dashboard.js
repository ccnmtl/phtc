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

        });
    }
    move_video_modules();

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
    $('.module').mouseover(function(event){
    	$(this).find('.show-descendants').css('display','block').mouseout(function() { 
    		$(this).css('display','none');
    });
    	

    // NYNJ -> is the course available?
    if (PHTC.getUrlVars().course_not_available === "true"){
        jQuery('#myModal').modal('toggle');
    }

});//end doc.ready
