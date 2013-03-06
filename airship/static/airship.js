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
groundstation.username = "Anonymous Coward";

groundstation.active_grefs = new Grefs();

var GrefMenuItem = Backbone.View.extend({
  tagname: "li",
  className: "gref",

  template: '<a class="select" href="#">{{identifier}}</a>',

  getUrl: function() {
    return "/gref/" + this.model.attributes["channel"] + "/" + this.model.attributes["identifier"];
  },

  render: function() {
    this.$el.html(this.template.replace("{{identifier}}", this.model.attributes["identifier"]));
    return this;
  },

  select: function() {
    rendered_gref.url = this.getUrl();
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

function buildCommentBox(div, model) {
  var input, submit;

  input = document.createElement("p");
  input.className = "github-issue-comment";
  input.contentEditable = true;
  input.id = "new-comment-body";

  submit = document.createElement("button");
  submit.className = "btn";
  submit.id = "new-comment-submit";
  submit.innerText = "Submit";

  $(submit).on('click', function(ev) {
    $.ajax({
        type: "POST",
        url: model.url,
        data: {
            body: input.innerText,
            parents: JSON.stringify([_.last(model.attributes.content).hash]),
            user: groundstation.username

        },
        success: function(data, st, xhr) {
            rendered_gref.fetch();
            console.log("Successfully updated groundstation");
        }
    });
    console.log("Sending new comment to groundstation");
  });

  div.appendChild(input);
  div.appendChild(submit);
}

var RenderedGref = Backbone.View.extend({

  tagName: "div",
  className: "",

  render: function() {
    console.log("Rendering new refs");
    var self = this;
    var content = this.model.attributes["content"];
    var root = this.model.attributes["root"];

    _.each(this.$el.children(), function(el) { el.remove(); });
    if (root.protocol.search("richo@psych0tik.net:github:" === 0)) {
      // Github issue
      render_github_issue(content, root, self.el);
    } else {
      console.log("Unhandled protocol: " + root.protocol);
      return this;
    }
    buildCommentBox(self.el, self.model);
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
