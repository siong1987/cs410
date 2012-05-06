MainView = function(current) {
  var out = '\
  <p>Your link <b>' + current.link + '</b> titled <b>' + current.title + '</b> is categorized as <b>' + current.category + '</b>\
  <a class="yes-button" href="#">Yes</a>\
  <a class="no-button" href="#">No</a>\
  '
  return out;
}
