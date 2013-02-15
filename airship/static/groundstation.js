var MyApp = angular.module('MyApp', []).
  config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'postList.html',
        controller: "PostListCtrl"
      }).
      when('/post/:id', {
        templateUrl: 'postShow.html',
        controller: "PostShowCtrl"
      }).
      when('/posts/add', {
        templateUrl: 'postAdd.html',
        controller: "PostAddCtrl"
      }).
      when('/post/:id/edit', {
        templateUrl: 'postEdit.html',
        controller: "PostEditCtrl"
      });
    $locationProvider.html5Mode(true);
  }]);

MyApp.controller('ChannelListCtrl', function ChannelListCtrl($scope, $http) {
  $http.get('/api/channels').
    success(function(data, status, headers, config){
      if(data.success){
        $scope.posts = data.posts;
      }
    });
});

angular.module('groundstation', []).
  directive('tabs', function() {
    return {
      restrict: 'E',
      transclude: true,
      scope: {},
      controller: function($scope, $element) {
        var panes = $scope.panes = [];

        $scope.select = function(pane) {
          angular.forEach(panes, function(pane) {
            pane.selected = false;
          });
          pane.selected = true;
        }

        this.addPane = function(pane) {
          if (panes.length == 0) $scope.select(pane);
          panes.push(pane);
        }
      },
      template:
        '<div class="tabbable">' +
          '<ul class="nav nav-tabs">' +
            '<li ng-repeat="pane in panes" ng-class="{active:pane.selected}">'+
              '<a href="" ng-click="select(pane)">{{pane.title}}</a>' +
            '</li>' +
          '</ul>' +
          '<div class="tab-content" ng-transclude></div>' +
        '</div>',
      replace: true
    };
  }).
  directive('pane', function() {
    return {
      require: '^tabs',
      restrict: 'E',
      transclude: true,
      scope: { title: '@' },
      link: function(scope, element, attrs, tabsCtrl) {
        tabsCtrl.addPane(scope);
      },
      template:
        '<div class="tab-pane" ng-class="{active: selected}" ng-transclude>' +
        '</div>',
      replace: true
    };
  })
