var RenderedGref = Backbone.View.extend({

  tagName: "div",
  className: "",

  render: function() {
    var self = this;
    _.each(this.$el.children(), function(el) { el.remove() })
    _.each(this.model.attributes["content"], function(item) {
      var el;
      if (item.type == "title") {
        el = document.createElement("h2");
        el.innerHTML = item.body;
      } else if (item.type == "body") {
        el = document.createElement("p");
        el.innerHTML = markdown.toHTML(item.body);
      } else if (item.type == "comment") {
        el = document.createElement("p");
        el.className = "github-issue-comment";
        el.setAttribute("data-author", item.user);
        el.innerHTML = markdown.toHTML(item.body);
      } else {
        console.log("Unhandled node of type: " + item.type);
      }
      if (el !== undefined) {
        self.el.appendChild(el);
      }
    });
    return this;
  },

  install: function() {
    $("#gref-content")[0].appendChild(this.el);
  },

  initialize: function() {
    this.listenTo(this.model, "change", this.render);
    this.install();
  }
});
