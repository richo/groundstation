function Groundstation() {
  this.channels = new Channels();
  this.channels.url = '/channels';

  this.active_grefs = new Grefs();

  this.username = localStorage.getItem("airship.committer") || "Anonymous Coward";

  this.renderers = {};
  this.validators = {};
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
  var new_gref = {
    title: $("#new-gref-title").text(),
    body: $("#new-gref-body")[0].value,
    name: $("#new-gref-name").text()
  };
  var new_gref_validator = groundstation.validators.gref(new_gref.name, new_gref.title, new_gref.body);

  $("#new-gref").on('click', function() {
    $("#new-gref-title").text(new_gref.title);
    $("#new-gref-body")[0].value = new_gref.body;
    $("#new-gref-name").text(new_gref.name);
    var modal = $("#new-gref-modal");
    modal.modal();
  });
  $("#new-gref-cancel").on('click', function() {
    $("#new-gref-modal").modal('hide');
  });
  $("#new-gref-create").on('click', function() {
    var title = $("#new-gref-title").text(),
        body = $("#new-gref-body")[0].value,
        name = $("#new-gref-name").text(),
        protocol = $("#new-gref-protocol").text();

    if (new_gref_validator(name, title, body)) {
      $.ajax({
        type: "PUT",
        url: groundstation.active_grefs.url,
        data: {
          title: title,
          body: body,
          name: name,
          protocol: protocol,

          user: groundstation.username

        },
        success: function(data, st, xhr) {
          $("#new-gref-modal").modal('hide');
          groundstation.active_grefs.redraw();
        }
      });
    } else {
      // TODO Actually give the user something to go with
      alert("Validation failed!");
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
    groundstation.active_grefs.redraw = function() {
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
    };
    groundstation.active_grefs.redraw();
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
  var row, input, span, submit;

  row = document.createElement("div");
  row.className = "input-group";

  input = document.createElement("textarea");
  input.setAttribute('rows', 7);
  input.contentEditable = true;
  input.id = "new-comment-body";

  span = document.createElement("span");
  span.className = "input-group-btn";

  submit = document.createElement("button");
  submit.className = "btn";
  submit.id = "new-comment-submit";
  $(submit).text("Submit");
  span.appendChild(submit);

  row.appendChild(input);
  row.appendChild(span);

  $(submit).on('click', function(ev) {
    $.ajax({
        type: "POST",
        url: model.url,
        data: {
            body: input.value,
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

  div.appendChild(row);
}

var RenderedGref = Backbone.View.extend({

  tagName: "div",
  className: "",

  render: function() {
    var self = this;
    var content = this.model.attributes["content"];
    var root = this.model.attributes["root"];
    var renderer = null;

    $(this.$el).children().remove();
    $("#gref-graph").children().remove();

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
      if (el) {
        el.setAttribute("id", item.hash);
        var signature = self.model.attributes.signatures[item.hash];
        if (signature !== undefined) {
          if (signature === false) {
            el.setAttribute("data-invalid-signature", "true");
          } else {
            el.setAttribute("data-signature", signature);
          }
        }
        self.el.appendChild(el);
      }
    });
    buildCommentBox(self.el, self.model);


    var graph_span = $("#gref-graph-span");
    var width  = graph_span.width(),
                              // 40 pix header, 20 pix footer
        height = document.documentElement.clientHeight - 60;

    var force = d3.layout.force()
      .charge(-120)
      .size([width, height])
      .linkDistance(30);

    var svg = d3.select("#gref-graph").append("svg")
      .attr("width", width)
      .attr("height", height);;

    var data = this.model.attributes;
    var nodes = data.content;
    data.root.parents = [];
    data.root.fixed = true;
    data.root.x = width / 2;
    data.root.y = 10;
    nodes.push(data.root);

    var hash_to_node = {};
    nodes.forEach(function(node) {
      hash_to_node[node.hash] = node;
    });

    var links = [];
    nodes.forEach(function(node) {
      node.parents.forEach(function(parent) {
        links.push({source: node, target: hash_to_node[parent]});
      });
    });

    var tip_node, tip_length = data.tips.length;
    for(var i = 0; i < tip_length; i++) {
      tip_node = hash_to_node[data.tips[i]];
      tip_node.y = height - 10;
      tip_node.x = (width / (tip_length + 1)) * (i + 1);
      tip_node.fixed = true;
    };

    force.nodes(nodes)
      .links(links)
      .start();

    var link = svg.selectAll(".link")
      .data(links)
      .enter().append("line")
      .attr("class", "link");

    function hilight(id) {
      hash_to_node[id].parents.forEach(function(par) {
        hilight(par);
      });
      $(document.getElementById(id)).addClass("selected");
    }

    var last_node = null;
    var node = svg.selectAll(".node")
      .data(nodes)
      .enter().append("circle")
      .attr("class", "node")
      .attr("r", 5)
      .call(force.drag)
      .on('click', function(node) {
        if (last_node !== null)
          d3.select(last_node).attr('r', 5);

        d3.select(this).attr('r', 10);
        last_node = this;

        $(".gref-taggable").removeClass("selected");
        hilight(node.hash);
      });

    force.on("tick", function() {
      link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

      node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

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
