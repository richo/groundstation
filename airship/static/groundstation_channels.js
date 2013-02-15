function RouteCtrl($route) {
  var self = this;

  $route.when('/channels', {template:'static/channels/list.html'});

  $route.when('/channels/:name', {template:'static/channels/show.html'});

  $route.otherwise({redirectTo:'/'});

  $route.parent(this);
}
