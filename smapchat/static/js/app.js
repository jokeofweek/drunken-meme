var chatApp = angular.module('Smapchat', ['goangular', 'ngRoute', 'smapchatControllers', 'ui.bootstrap']);

chatApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

chatApp.config(function($goConnectionProvider) {
  $goConnectionProvider.$set('https://goinstant.net/90cc363c5211/mchacks');
});

chatApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
    when('/', {
      templateUrl: '/static/partials/loading.html',
      controller: 'SmapchatCtrl'
    }).
    when('/none',  {
      templateUrl: '/static/partials/nomaps.html',
      controller: 'SmapchatNoMapsCtrl'
    }).
    when('/chat/:chatIndex',  {
      templateUrl: '/static/partials/chat.html',
      controller: 'SmapchatChatCtrl'
    }).

    when('/map/:mapIndex',  {
      templateUrl: '/static/partials/map.html',
      controller: 'SmapchatMapCtrl'
    });
}]);

