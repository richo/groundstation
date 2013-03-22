groundstation.plumbers.push((function() {
    function build_anchor(side) {
        return {
            connector:"StateMachine",
            paintStyle:{lineWidth:3,strokeStyle:"#056"},
            endpoint:"Blank",
            anchor:[[side, 0, 1, 0], [side, 1, 1, 0]],
            overlays:[ ["PlainArrow", {location:1, width:7, length:3} ]]
        };
    }
    var anchors = {
        0: build_anchor(0),
        1: build_anchor(1)
    };
    return function(content) {
        var links = {};
        var side = 1;
        _.each(content, function(item) {
          _.each(item.parents, function(parent_id) {
            if (links[parent_id] === undefined)
              links[parent_id] = [parent_id];
            else {
              links[parent_id].push(parent_id);
              side++;
            }

            if ($("#" + parent_id).length > 0) {
              console.log("Creating links");
              item.connections.push(jsPlumb.connect({
                source:item.hash,
                target:parent_id
              }, anchors[side % 2]));
            } else {
              console.log("Not creating links, pretty sure it's a root node");
            }
          });
        });
    };
})());
