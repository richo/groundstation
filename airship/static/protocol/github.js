groundstation.renderers["richo@psych0tik.net:github:"] = function (item) {
  var classFor = function(ev) {
    if (ev == "reopened")
      return "alert alert-success";
    else if (ev == "closed")
      return "alert alert-error";
    else
      return "alert";
  };
  var el;
  if (item.type == "title") {
    el = document.createElement("div");

    op = document.createElement("div");
    op.className = "alert alert-info";
    op.innerText = "opened by " + item.user;
    el.appendChild(op);

    ti = document.createElement("h2");
    ti.innerHTML = item.body;
    el.appendChild(ti);
  } else if (item.type == "body") {
    if (item.body !== null) {
      el = document.createElement("p");
      el.innerHTML = markdown.toHTML(item.body);
    }
  } else if (item.type == "comment") {
    el = document.createElement("p");
    el.className = "github-issue-comment gref-taggable";
    el.setAttribute("data-author", item.user);
    el.setAttribute("data-hash", item.hash);
    el.innerHTML = markdown.toHTML(item.body);
  } else if (item.type == "event") {
    el = document.createElement("div");
    el.className = "gref-taggable";
    el.className += ' ' + classFor(item.state);
    el.innerText = item.state + " by " + item.user;
    el.setAttribute("data-hash", item.hash);
  } else {
    console.log("Unhandled node of type: " + item.type);
  }
  if (item.signature !== undefined && item.signature !== false) {
    el.setAttribute("data-sigature", item.signature);
  }
  return el;
};
