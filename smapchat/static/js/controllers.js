var smapchatControllers = angular.module('smapchatControllers', []);

smapchatControllers.controller('SmapchatCtrl', function($scope, $goKey, $http, $location, $rootScope, $window) {

  var id = window.location.href.replace('#' + $location.path(), '').split('/').pop();
  $rootScope.EVENT_ID = id;
  $rootScope.USER_ID = $window.USER_ID;
  $rootScope.Math = window.Math;

  $scope.loading = true;
  $rootScope.messages = $goKey('messages');
  $rootScope.messages.$sync();
  $rootScope.savedPins = $goKey('savedPins3l  ');
  $rootScope.savedPins.$sync();

  $rootScope.myPin = null;
  $rootScope.mapIndex = null;

  $rootScope.isSelectedMap = function(index){
    return index == $rootScope.mapIndex;
  };

  var dataSynced = Q.defer();

  $scope.messages.$on('ready', function() {
    dataSynced.resolve();
  });


  Q.all([
    $http.get('/event/' + id + '.json'),
    dataSynced
  ]).catch(function(err) {
    document.location.href = '/'; 
  }).done(function(results) {
    $rootScope.eventInformation = results[0].data;

    // If there are no maps, load the nomap partial.
    if ($rootScope.eventInformation.maps.length === 0) {
      $location.path('/none');
    } else {
      $location.path('/map/0');
    }
    $scope.loading = false;
  });
});

smapchatControllers.controller('SmapchatNoMapsCtrl', function($scope, $goKey, $http, $location) {

});

smapchatControllers.controller('SmapchatMapCtrl', function($scope, $goKey, $http, $location, $routeParams, $rootScope, $aside, $window) {
  $rootScope.Math = window.Math;
  $rootScope.mapIndex = $routeParams.mapIndex;
  $rootScope.map = $rootScope.eventInformation.maps[parseInt($rootScope.mapIndex)]
  $scope.imageWidth = 1;
  $scope.imageHeight = 1;
  $rootScope.USER_ID = $window.USER_ID;

  $scope.clickMapPosition = function(arg){
    var isFirst = false;
    if (!$rootScope.myPin) {
      $rootScope.myPin = {};
      isFirst = true;
    }

    $scope.imageWidth = arg.target.width;
    $scope.imageHeight = arg.target.height

    var x = arg.offsetX / $scope.imageWidth;
    var y =  arg.offsetY / $scope.imageHeight;

    $rootScope.myPin.x = arg.offsetX / $scope.imageWidth;
    $rootScope.myPin.y = arg.offsetY / $scope.imageHeight;
    $rootScope.myPin.userId = $window.USER_ID;
    $rootScope.savedPins.$add({x:x, y:y, id: $window.USER_ID});
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