var smapchatControllers = angular.module('smapchatControllers', []);

smapchatControllers.controller('SmapchatCtrl', function($scope, $goKey, $http, $location, $rootScope) {
  $scope.loading = true;
  $scope.messages = $goKey('messages');
  $scope.messages.$sync();

  $rootScope.currentMap = null;

  $rootScope.isSelectedMap = function(index){
    return index == $rootScope.currentMap;
  }

  var dataSynced = Q.defer();

  $scope.messages.$on('ready', function() {
    dataSynced.resolve();
  });


  Q.all([
    $http.get('/event/1.json'),
    dataSynced
  ]).done(function(results) {
    $scope.eventInformation = results[0].data;

    // If there are no maps, load the nomap partial.
    if ($scope.eventInformation.maps.length === 0) {
      $location.path('/none');
    } else {
      $location.path('/map/0');
    }
    $scope.loading = false;
  })
});

smapchatControllers.controller('SmapchatNoMapsCtrl', function($scope, $goKey, $http, $location) {

});

smapchatControllers.controller('SmapchatMapCtrl', function($scope, $goKey, $http, $location, $routeParams, $rootScope) {
  $rootScope.currentMap = $routeParams.mapIndex;

  $scope.sendMessage = function() {
    var message = {
      content: $scope.messageContent,
      author: $scope.author
    };

    // Each method returns a promise, we can use that to confirm that item was
    // added successfully
    $scope.messages.$add(message).then(function() {
      $scope.messageContent = '';
    });
  }
});