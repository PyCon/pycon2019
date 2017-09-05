$(document).ready(function() {

  // add class to body so we know when js is loaded
  $('body').addClass('js');

  var nav = $('#nav'),
      navToggle = $('#nav-toggle'),
      dropdownToggle = $('.nav-primary-link');

  navToggle.click(function(e) {
    e.preventDefault();
    $(this).toggleClass('open');
    $(this).next(nav).toggle();
  });

  dropdownToggle.click(function(e) {
    $(this).toggleClass('open');
    $(this).next('.dropdown-menu').toggle();
    $('.dropdown-menu').not($(this).siblings()).hide();
    $(dropdownToggle).not($(this)).removeClass('open');
    e.stopPropagation();
  });

  $('html').click(function() {
    $('.dropdown-menu').hide();
    $('.dropdown-menu').removeClass('open');
    dropdownToggle.removeClass('open');
  });

});

