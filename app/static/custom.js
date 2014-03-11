// Register FastClick
$(function () {
    FastClick.attach(document.body);
});

$(document).ready(function () {
    // Show active Nav element
    var link_selector = 'a[href="' + window.location.pathname + '"]';
    $('ul#nav_ul').find(link_selector).parent().addClass('active');

    // Animate Logo
    var animation_classes = 'animated wobble';
    var $logo = $('#logo');
    $logo.click(function () {
        $logo.addClass(animation_classes);
        $logo.one('webkitAnimationEnd mozAnimationEnd oAnimationEnd animationEnd', function () {
            $logo.removeClass(animation_classes);
        });
    });
});

delete_serving = function (url, serving_id) {
    jqxhr = $.ajax({
        url: url,
        type: 'DELETE'
    });
    jqxhr.success(function () {
        console.log('Successfully deleted: ' + serving_id);
        location.reload();
    });
    jqxhr.error(function () {
        console.log("Delete request didn't work: " +  serving_id)
    });
};
