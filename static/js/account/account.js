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
    $scope.categories = [];
    $scope.types = [];

    $scope.initData = function() {
        accountService.getTransactions($routeParams['id']).then(function (result) {
            $scope.transactions = result.data.response;
            $scope.account = result.data.account;
        });
    };

    $scope.deleteTransaction = function(transactionId) {
        accountService.deleteTransaction(transactionId).then(function (result) {
           $scope.initData();
        });
    };

    $scope.loadCategories = function() {
        return accountService.getTransactionCategories().then(function (result) {
            $scope.categories = result.data.response;
        });
    };

    accountService.getTransactionTypes().then(function(result) {
        $scope.types = result.data.response;
    });

    $scope.saveTransaction = function(data, id) {
        //$scope.user not updated yet
        angular.extend(data, {id: id});
        return accountService.postTransaction(data);
    };
});