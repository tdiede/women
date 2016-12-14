"use strict";

$('nav').hide();


$('.fa-bars').on('click', showNav);

function showNav(e) {
    $('nav').toggle();
}
