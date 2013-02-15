var Channel = Backbone.Model.extend();

var Channels = Backbone.Collection.extend({
  model: Channel
});

var ChannelTab = Backbone.View.extend({

  tagName: "div",

  className: "channel-tab",

  template: '<div class="tabbable">' +
      '<ul class="nav nav-tabs">' +
        '<li ng-repeat="pane in panes" ng-class="{active:pane.selected}">'+
          '<a href="" ng-click="select(pane)">{{name}}</a>' +
        '</li>' +
      '</ul>' +
      '<div class="tab-content" ng-transclude></div>' +
    '</div>'
  ,

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
