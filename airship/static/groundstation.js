var Channel = Backbone.Model.extend();

var Channels = Backbone.Collection.extend({
  model: Channel
});

var ChannelTab = Backbone.View.extend({

  tagName: "div",

  className: "channel-tab",

  template: '<li style="text-shadow: none;" class=""><a href="#" style="text-shadow: none;">{{name}}</a></li>',

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
    $('#content')[0].appendChild(this.el);
  },

  initialize: function() {
    this.listenTo(this.model, "change", this.render);
    this.render();
    this.install();
  }

});

groundstation_channels = new Channels();
groundstation_channels.url = '/channels';
