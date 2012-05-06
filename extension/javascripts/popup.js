document.addEventListener('DOMContentLoaded', function () {
  chrome.tabs.getSelected(null, function(tab) {
    var tab_url = tab.url;
    Classifier.understandLink(tab_url, function(result) {
      var current = {
        title: result.title,
        link: tab_url,
        category: result.category
      }
      main_controller = new MainController(current);
      main_controller.render();
    });
  });
});

