var app = angular.module('LadderApp', ['ngResource']);

app.controller('LadderView', function($scope) {

});

app.factory('Players', function($resource) {
  return $resource('/players/:playerId', {playerId:'@id'}, {
    update: {
      method: 'POST'
    }
  });
});

app.factory('Ladder', function() {
  return $resource('/standings');
});

app.factory('Results', function() {
  return $resource('/result');
});
