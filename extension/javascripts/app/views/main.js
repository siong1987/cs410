MainView = function(current) {
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
          <tr>\
            <td>is categorized as <b>' + current.category + '</b></td>\
          </tr>\
          <tr>\
            <td>\
              <button type="button" id="no-button" class="btn">No</button>\
              <button type="button" id="yes-button" class="btn btn-primary">Confirm Category</button>\
            </td>\
          </tr>\
        </table>\
      </td>\
    </tr>\
  </table>\
  '
  return out;
}
