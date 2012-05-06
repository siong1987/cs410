MainController = Backbone.View.extend({
  current: {},

  events: {
    "click .yes-button": "yesButton",
    "click .no-button": "noButton"
  },

  yesButton: function(e) {
    e.preventDefault();

    // create the bookmark
    //Classifier.trainLink(self.current.link, self.current.category, function() {
      window.close();
    //});
  },

  noButton: function(e) {
    e.preventDefault();

    update_controller = new UpdateController(self.current);
    update_controller.render();
  },

  initialize: function(cur) {
    self.current = cur;
  },

  render: function() {
    $(this.el).html(MainView(self.current));
    $('body').html(this.el);
  }
});

