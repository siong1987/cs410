UpdateController = Backbone.View.extend({
  current: {},

  events: {
    "click #cancel-button": "cancel",
    "click #update-button": "update"
  },

  initialize: function(cur) {
    self.current = cur;
  },

  cancel: function(e) {
    e.preventDefault();
    window.close();
  },

  update: function(e) {
    e.preventDefault();
    category = $('.new-category').val();
    self.current.category = category;

    // create the bookmark
    Classifier.trainLink(self.current.link, self.current.category, function() {
      Bookmark.add(self.current);
      window.close();
    });
  },

  render: function() {
    $(this.el).html(UpdateView());
    $('body').html(this.el);
  }
});

