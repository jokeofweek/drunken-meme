var smapchatControllers = angular.module('smapchatControllers', []);

var preloadInformation = function($scope, $goKey, $http, $location, callback) {
  $scope.loading = true;
  $scope.messages = $goKey('messages');
  $scope.messages.$sync();

  if ($scope.eventInformation) {
    callback([{'data': $scope.eventInformation}]);
  } else { 
    var dataSynced = Q.defer();

    $scope.messages.$on('ready', function() {
      dataSynced.resolve();
    });

    var id = window.location.href.replace('#' + $location.path(), '').split('/').pop();

    return Q.all([
      $http.get('/event/' + id + '.json'),
      dataSynced
    ]).catch(function(err) {
      document.location.href = '/'; 
    }).done(callback)
  }
}

smapchatControllers.controller('SmapchatCtrl', function($scope, $goKey, $http, $location, $rootScope) {
  $rootScope.mapIndex = null;

  $rootScope.isSelectedMap = function(index){
    return index == $rootScope.mapIndex;
  }

  preloadInformation($scope, $goKey, $http, $location, function(results) {
    $rootScope.eventInformation = results[0].data;

    // If there are no maps, load the nomap partial.
    if ($location.path() == '/') {
      if ($rootScope.eventInformation.maps.length === 0) {
        $location.path('/none');
      } else {
        $location.path('/map/0');
      }
    }
    $scope.loading = false;
  });
});

smapchatControllers.controller('SmapchatNoMapsCtrl', function($scope, $goKey, $http, $location) {

});

smapchatControllers.controller('SmapchatMapCtrl', function($scope, $goKey, $http, $location, $routeParams, $rootScope) {
  $rootScope.mapIndex = $routeParams.mapIndex;

  preloadInformation($scope, $goKey, $http, $location, function(results) {
    $rootScope.eventInformation = results[0].data;

    // If there are no maps, load the nomap partial.
    if ($rootScope.eventInformation.maps.length === 0) {
      $location.path('/none');
    } else {
      $rootScope.map = $rootScope.eventInformation.maps[parseInt($rootScope.mapIndex)] 
    }
    $scope.loading = false;
  });

  $scope.selectMapPoint = function() {
    console.log($event);
  };
});

smapchatControllers.controller('SmapchatChatCtrl', function($scope, $goKey, $http, $location, $routeParams, $rootScope) {
  $rootScope.mapIndex = $routeParams.mapIndex;
  $rootScope.map = $rootScope.eventInformation.maps[parseInt($rootScope.mapIndex)]

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