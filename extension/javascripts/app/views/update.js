UpdateView = function() {
  var out = '\
  <p>What category do you think the link <b>' + current.link + '</b> titled <b>' + current.title + '</b> belongs to?\
  <input type="text" class="new-category" />\
  <a class="update-button" href="#">Update</a>\
  <a class="cancel-button" href="#">Cancel</a>\
  ';
  return out;
}

