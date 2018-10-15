/* globals hljs, axios, Cookies */

$(document).ready(function () {
  // https://highlightjs.org/usage/
  $('pre code').each(function (i, block) {
    hljs.highlightBlock(block);
  });

  // tooltip por defecto.
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });

  // navbar-search
  // Muestra el input search.
  $('.navbar-search-button').on('click', function () {
    $('.navbar-search').removeClass('hidden');
    $('.navbar-search-input').focus();
  });

  $('.navbar-search-close').on('click', function () {
    $('.navbar-search').addClass('hidden');
  });
});

// Vue vars.
const delimiters = ['${', '}'];

// csrf axios
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

// csrf Ajax.
const csrfToken = $('[name=csrfmiddlewaretoken]').val();

// TODO: Mejorar
$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
  }
});
