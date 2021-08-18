const button = $('.button'),
  spinner = '<span class="spinner"></span>';

document.getElementById('button').onclick = () => {
  if (!button.hasClass('loading')) {
    button.toggleClass('loading').html(spinner);
  }
  else {
    button.prop('disabled', true);
  }
}
