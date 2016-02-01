'use strict';

function $apiRoot() {
    return $("#linkApiRoot").attr("href");
}

// Declare app level module which depends on views, and components
angular.module('myCashManager', [
  'ngRoute',
  'myCashManager.dash',
  'myCashManager.account',
  'myCashManager.version',
  'myCashManager.commonServices',
  'myCashManager.accountServices',
  'myCashManager.category'
]).config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/dash'});
}]);

