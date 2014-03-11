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
        // If you don't do the following, you wobble once and you're done forever
        $logo.one('webkitAnimationEnd mozAnimationEnd oAnimationEnd animationEnd', function () {
            $logo.removeClass(animation_classes);
        });
    });
});

// Aquire CSRF-Token from cookie
// See https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

delete_serving = function (url, serving_id) {
    jqxhr = $.ajax({
        url: url,
        type: 'DELETE',
        crossDomain: false,
        headers: {'X-CSRFToken': csrftoken}
    });
    jqxhr.success(function () {
        console.log('Successfully deleted: ' + serving_id);
        location.reload();
    });
    jqxhr.error(function () {
        console.log("Delete request didn't work: " + serving_id)
    });
};
