'use strict';

angular.module('myCashManager.dash',
    ['ngRoute', 'ngAnimate', 'ui.bootstrap']
).config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/dash', {
    templateUrl: $apiRoot() + 'dash/dash.html',
    controller: 'DashCtrl'
  });
}]).controller('DashCtrl', function($scope,
                                    $uibModal,
                                    $log,
                                    $location,
                                    appService,
                                    accountService) {

    $scope.accounts = [];

    $scope.getAccounts = function() {
        accountService.getAccounts().then(function (result) {
            $scope.accounts = result.data.response;
        });
    };

    $scope.items = ['item1', 'item2', 'item3'];

    $scope.animationsEnabled = true;

    $scope.open = function (size) {

        var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: appService.apiRoot() + 'dash/addAccountContent.html',
            controller: 'ModalCreateAccountCtrl',
            size: size,
            resolve: {
                items: function () {
                    return $scope.items;
                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
            accountService.putAccount($scope.selected)
                .then(function () {
                    $scope.getAccounts();
                });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.openTransactionContent = function (accountId) {

        var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: appService.apiRoot() + 'dash/addTransactionContent.html',
            controller: 'ModalAddTransactionCtrl',
            resolve: {
                accountId: function() {
                    return accountId;
                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
            accountService.putTransaction($scope.selected)
                .then(function () {
                    $scope.getAccounts();
                });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.viewAccount = function (accountId) {
        $location.path('/account/'+accountId);
    };

    $scope.toggleAnimation = function () {
        $scope.animationsEnabled = !$scope.animationsEnabled;
    };
});