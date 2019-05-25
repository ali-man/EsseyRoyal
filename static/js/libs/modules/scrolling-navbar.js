"use strict";

(function ($) {
  var SCROLLING_NAVBAR_OFFSET_TOP = 50;
  $(window).on('scroll', function () {
    var $navbar = $('.navbar');

    if ($navbar.length) {
      if ($navbar.offset().top > SCROLLING_NAVBAR_OFFSET_TOP) {
        $('.scrolling-navbar').addClass('bg-block');
      } else {
        $('.scrolling-navbar').removeClass('bg-block');
      }
    }
  });
})(jQuery);