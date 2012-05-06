Classifier = {
  understandLink: function(link, cb) {
    $.ajax({
      type: 'POST',
      url: 'http://cs410.herokuapp.com/understand/link',
      data: {
        link: link
      },
      dataType: 'json'
    }).success(function(result) {
      cb(result);
    });
  },

  trainLink: function(link, category, cb) {
    $.ajax({
      type: 'POST',
      url: 'http://cs410.herokuapp.com/understand/link',
      data: {
        link: link,
        category: category
      },
      dataType: 'json'
    }).success(function(result) {
      cb(result);
    });
  },
};

