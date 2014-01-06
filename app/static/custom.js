//Register FastClick
$(function () {
    FastClick.attach(document.body);
});

$(document).ready(function () {
    var link_selector = 'a[href="' + window.location.pathname + '"]';
    $('ul#nav_ul').find(link_selector).parent().addClass('active');
});
