Bookmark = {
  root: null,
  init: function() {
    chrome.bookmarks.getTree(
    function(bookmarkTree) {
      var bookmark_bar = bookmarkTree[0].children[0];
      var is_exist = false;
      _.each(bookmark_bar.children, function(node) {
        if (node.title === 'Booksmarter') {
          self.root = node;
          is_exist = true;
        }
      });
      if (!is_exist) {
        chrome.bookmarks.create({
          'parentId': bookmark_bar.id,
          'title': 'Booksmarter'
        },
        function(node) {
          self.root = node;
        });
      }
    }
  )},

  add: function(current) {
    var is_exist = false;
    var category_node = null;
    _.each(self.root.children, function(node) {
      if (node.title === current.category) {
        category_node = node;
        is_exist = true;
      }
    });
    if (!is_exist) {
      chrome.bookmarks.create({
        'parentId': self.root.id,
        'title': current.category
      },
      function(node) {
        chrome.bookmarks.create({
          'parentId': node.id,
          'title': current.title,
          'url': current.link
        });
      });
    }
  }
};

Bookmark.init();

