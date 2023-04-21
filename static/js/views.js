$(function(){
    $('button.state-button').on('click', function(){
        var $target = $(this).attr('data-target');
        var $targetSelector = 'section#' + $target;
        $($targetSelector).attr('class', 'state-visible');
        $('section.state:not(' + $targetSelector + ')').attr('class', 'state-hidden')
    })
});