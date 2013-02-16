var Channel = Backbone.Model.extend();

var Channels = Backbone.Collection.extend({
  model: Channel
});

var ActiveChannel = Backbone.View.extend({
  tagName: "div",
  className: "active-channel",
  template: '<div class="container">{{content}}</div>',

  render: function() {
    this.$el.html(this.template.replace("{{content}}", this.model.attributes["data"]));
    $("#main-data").first.html($this.$el.html);
  },

  initialize: function() {
    this.listenTo(this.model, "change", this.render);
    this.render();
  }

});

var ChannelTab = Backbone.View.extend({

  tagName: "li",

  className: "",

  template: '<a href="#">{{name}}</a>',

  render: function() {
    this.$el.html(this.template.replace("{{name}}", this.model.attributes["name"]));
    return this;
  },

  select: function() {
    // Callback to inspect this node goes here
  },

  events: {
    "click .nav":          "select"
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

groundstation_channels = new Channels();
groundstation_channels.url = '/channels';
