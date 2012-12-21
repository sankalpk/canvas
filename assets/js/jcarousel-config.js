jQuery(document).ready(function(){
	function mycarousel_initCallback(carousel) {
		jQuery('.jcarousel-control a').bind('click', function() {
        carousel.scroll(jQuery.jcarousel.intval(jQuery(this).text()));
        return false;
		});
		
		jQuery('#tscarousel-next').bind('click', function() {
			carousel.next();
			return false;
		});
	
		jQuery('#tscarousel-prev').bind('click', function() {
			carousel.prev();
			return false;
		});
	};

	jQuery('#tscarousel').jcarousel({
        scroll: 1,
		wrap:"both",
        initCallback: mycarousel_initCallback
    });
							
});