var smapchatControllers = angular.module('smapchatControllers', []);

smapchatControllers.controller('SmapchatCtrl', function($scope, $goKey, $http, $location) {
  $scope.loading = true;
  $scope.messages = $goKey('messages');
  $scope.messages.$sync();

  $scope.map = null;

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
    $location.path('/none');
    $scope.loading = false;
  })

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