jQuery(document).ready(function() {

    function generateModalNav() {
        var modalSet;
        
        modalSet = [
            {"modalContentPath":"/sadowl/","modalTitle":"Sad Owl"},
            {"modalContentPath":"/roostercat/","modalTitle":"Rooster Cat"},
            {"modalContentPath":"/nyancat/","modalTitle":"Nyan Cat"}
        ];
        
        for (i=0; i<modalSet.length; i++) {
            jQuery('.modalpageNav').append('<a href="'+modalSet[i].modalContentPath+'" role="button" class="btn btn-mini btn-primary" data-toggle="modal" data-target="#modalBox"'+i+1+'>'+modalSet[i].modalTitle+'</a> ');
        }
    
        jQuery('.modalpageNav').append('<div class="modal hide" id="modalBox"></div>');
    }
    
    function launchModalPage() {
        var srcElement;
        jQuery('.modalpageNav').click(function(evt){
            srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var modalTarget = jQuery(srcElement).attr('data-target');
            var contentPath = jQuery(srcElement).attr('href');
            jQuery(modalTarget).html('');
            jQuery(modalTarget).load(contentPath);
        });
    }
    
    generateModalNav();
    launchModalPage();
});


