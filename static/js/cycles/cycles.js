'use strict';

angular
.module('myCashManager.cycles', ['ngRoute'])
.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/cycles', {
        templateUrl: $apiRoot() + 'cycles/cycles.html',
        controller: 'CyclesCtrl'
    });
}]).controller('CyclesCtrl', function ($scope, $uibModal, $log, appService, accountService) {

    $scope.cycles = [];

    $scope.getCycles = function() {
        accountService.getCycles()
            .then(function (result) {
               $scope.cycles = result.data.response;
            });
    };

    $scope.open = function (size) {

        var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: appService.apiRoot() + 'cycles/add_cycle_content.html',
            controller: 'ModalAddCycleCtrl',
            size: size,
            resolve: {
                items: function () {
                    return $scope.items;
                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
            accountService.putCycle($scope.selected)
                .then(function () {
                    $scope.getCycles();
                });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

    $scope.openAddTransactionContent = function (cycle) {

        var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: appService.apiRoot() + 'cycles/add_transaction_content.html',
            controller: 'ModalAddCycleTransactionCtrl',
            //size: size,
            resolve: {
                cycle: function () {
                    return cycle;
                }
            }
        });

        modalInstance.result.then(function (selectedItem) {
            $scope.selected = selectedItem;
            accountService.putCycleTransaction($scope.selected)
                .then(function () {
                    $scope.getCycles();
                });
        }, function () {
            $log.info('Modal dismissed at: ' + new Date());
        });
    };

});