var Channel = Backbone.Model.extend();

var Channels = Backbone.Collection.extend({
  model: Channel
});

groundstation_channels = new Channels();
groundstation_channels.url = '/channels';
