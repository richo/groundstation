var groundstation = {};
var Channel = Backbone.Model.extend();

var Channels = Backbone.Collection.extend({
  model: Channel
});

var Gref = Backbone.Model.extend();

var Grefs = Backbone.Collection.extend({
  model: Gref
});

groundstation.channels = new Channels();
groundstation.channels.url = '/channels';

groundstation.active_grefs = new Grefs();

var GrefMenuItem = Backbone.View.extend({
  tagname: "li",
  className: "gref",

  template: '<a class="select" href="#">{{identifier}}</a>',

  render: function() {
    this.$el.html(this.template.replace("{{identifier}}", this.model.attributes["identifier"]));
    return this;
  },

  select: function() {
    var gref_location = "/gref/" + this.model.attributes["channel"] + "/" + this.model.attributes["identifier"];
    rendered_gref.url = gref_location;
    rendered_gref.fetch({
      success: function(model, response, options) {
        rendered_gref_content.render();
      }
    });
  },

  events: {
    "click .select":  "select"
  },

  install: function() {
    $('#current-grefs')[0].appendChild(this.el);
  },

  initialize: function() {
    this.listenTo(this.model, "change", this.render);
    this.render();
    this.install();
  }
});

var visible_grefs = [];
var ChannelTab = Backbone.View.extend({

  tagName: "li",

  className: "",

  template: '<a class="select" href="#">{{name}}</a>',

  render: function() {
    this.$el.html(this.template.replace("{{name}}", this.model.attributes["name"]));
    return this;
  },

  select: function() {
    var current_grefs = $("#current-grefs")[0];
    groundstation.active_grefs.url = '/grefs/' + this.model.attributes["name"];
    groundstation.active_grefs.fetch({
      success: function(collection, response, options) {
        $("#gref-container").show();
        _.each(visible_grefs, function(el) { el.remove(); });
        _.each(collection.models, function(gref) {
          visible_grefs.push(new GrefMenuItem({
            model: gref
          }));
        });
      }
    });
  },

  events: {
    "click .select":          "select"
  },

  install: function() {
    $('#channels-content')[0].appendChild(this.el);
  },

  initialize: function() {
    this.listenTo(this.model, "change", this.render);
    this.render();
    this.install();
  }

});

var RenderedGref = Backbone.View.extend({

  tagName: "div",
  className: "",

  render: function() {
    var self = this;
    _.each(this.$el.children(), function(el) { el.remove(); });
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
        el.setAttribute("data-hash", item.hash);
        // el.setAttribute("data-author", item.user);
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
var rendered_gref = new Gref();
var rendered_gref_content;
