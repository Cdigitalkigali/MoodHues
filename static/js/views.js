$(function(){
    //when a button is clicked
    $('.state-button').on('click', function(){
        // Get the target state
        var $target = $(this).attr('data-target');
        var $targetSelector = 'section#' + $target;
        // Show target state
        $($targetSelector).removeClass('state-hidden');
        $($targetSelector).addClass('state-visible');
        // Hide everything else
        $('section.state:not(' + $targetSelector + ')').removeClass('state-visible');
        $('section.state:not(' + $targetSelector + ')').addClass('state-hidden');
    })
});