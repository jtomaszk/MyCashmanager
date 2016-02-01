'use strict';

angular.module('myCashManager.account', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/account/:id', {
    templateUrl: $apiRoot() + 'account/account.html',
    controller: 'AccountCtrl'
  });
}]).controller('AccountCtrl', function($scope, $routeParams, accountService) {
    $scope.transactions = [];
    $scope.account = [];

    $scope.initData = function() {
        accountService.getTransactions($routeParams['id']).then(function (result) {
            $scope.transactions = result.data.response;
            $scope.account = result.data.account;
        });
    };
});