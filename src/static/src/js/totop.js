// // to-top
(function () {
  const offset = 150;
  const duration = 700;

  $(window).scroll(function () {
    if ($(this).scrollTop() > offset) {
      $('.to-top').removeClass('hidden');
    } else {
      $('.to-top').addClass('hidden');
    }
  });

  $('.to-top').click(function (event) {
    event.preventDefault();
    $('html, body').animate({ scrollTop: 0 }, duration);
    return false;
  });
})();
