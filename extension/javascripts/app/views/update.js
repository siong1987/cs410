UpdateView = function() {
  var out = '\
  <table class="main_frame">\
    <tr>\
      <td class="tb_text_center">\
        <table class="tb_center_width">\
          <tr>\
            <td class="cell_th">URL\:</td><td class="cell_td">' + current.link + '</td>\
          </tr>\
          <tr>\
            <td class="cell_th">Title\:</td><td class="cell_td">' + current.title + '</td>\
          </tr>\
        </table>\
        <table class="tb_center_width">\
          <tr><td class="empty_row"></td></tr>\
          <tr>\
            <td>\
              <input type="text" class="new-category" placeholder="New Category"/>\
            </td>\
          </tr>\
          <tr>\
            <td>\
              <button type="button" id="cancel-button" class="btn">Cancel</button>\
              <button type="button" id="update-button" class="btn btn-primary">Update</button>\
            </td>\
          </tr>\
        </table>\
      </td>\
    </tr>\
  </table>\
  ';
  return out;
}

