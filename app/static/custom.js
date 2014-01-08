// Register FastClick
$(function () {
    FastClick.attach(document.body);
});

$(document).ready(function () {
    // Show active Nav element
    var link_selector = 'a[href="' + window.location.pathname + '"]';
    $('ul#nav_ul').find(link_selector).parent().addClass('active');

    // Animate Logo
    var animation_classes = 'animated wobble'
    var $logo = $('#logo');
    $logo.click(function () {
        $logo.addClass(animation_classes);
        $logo.one('webkitAnimationEnd mozAnimationEnd oAnimationEnd animationEnd', function () {
            $logo.removeClass(animation_classes);
        });
    });
});
