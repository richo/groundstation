function Groundstation() {
  this.channels = new Channels();
  this.channels.url = '/channels';

  this.active_grefs = new Grefs();

  this.username = localStorage.getItem("airship.committer") || "Anonymous Coward";

  this.renderers = {};
}
function init_airship(groundstation) {
  _.each(groundstation.channels.models, function(channel) {
    new ChannelTab({
      model: channel,
        id: channel.attributes["name"]
    });
  });
  rendered_gref_content = new RenderedGref({
    model: rendered_gref
  });
  // Wire up user switching
  // TODO Currently not stored because I haven't decided where it should live. PRobably git-config(5)

  $("#current-user-name").html(groundstation.username);
  $("#current-user-name").on('click', function() {
    var username = prompt("Username for committing:");
    if (username !== null) {
      groundstation.username = username;
      $("#current-user-name").html(groundstation.username);
      try {
        localStorage.setItem("airship.committer", username);
      } catch (e) {
        console.log("Not setting committer name in localStorage");
      }
    }
  });
}

var Channel = Backbone.Model.extend();
var Channels = Backbone.Collection.extend({
  model: Channel
});


var Gref = Backbone.Model.extend();
var Grefs = Backbone.Collection.extend({
  model: Gref
});


var GrefMenuItem = Backbone.View.extend({
  tagName: "li",
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
    var active_el = this.el;
    $(this.el.parentElement.children).removeClass("active");
    rendered_gref.url = this.getUrl();
    rendered_gref.fetch({
      success: function(model, response, options) {
        $(active_el).addClass("active");
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
    var self = this;
    var current_grefs = $("#current-grefs")[0];
    groundstation.active_grefs.url = '/grefs/' + this.model.attributes["name"];
    groundstation.active_grefs.fetch({
      success: function(collection, response, options) {
        $("#active-channel").html(self.model.attributes["name"]);
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
            parents: JSON.stringify(model.attributes["tips"]),
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
    var renderer = null;

    $(this.$el).children().remove();
    renderer = (function() {
      for (var renderer in groundstation.renderers) {
        if (groundstation.renderers.hasOwnProperty(renderer)) {
          if (root.protocol.search(renderer) === 0)
            return groundstation.renderers[renderer];
        }
      }
    })();
    if (renderer === null) {
      console.log("Unhandled protocol: " + root.protocol);
      return this;
    }

    // Stick the root object in the DOM to make parent linking sane.
    (function() {
      var el = document.createElement("div");
      el.setAttribute("id", root.hash);
      self.el.appendChild(el);
    })();

    _.each(content, function(item) {
      var el = renderer(item);
      el.setAttribute("id", item.hash);
      if (el) {
        self.el.appendChild(el);
      }
    });
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
