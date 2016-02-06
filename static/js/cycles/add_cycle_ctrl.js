/**
 * Created by jarema-user on 2016-01-30.
 */

angular.module('myCashManager.cycles')
    .controller('ModalAddCycleCtrl',
    function ($scope, $uibModalInstance, items, accountService) {

    $scope.accounts = [];
    $scope.transactionTypes = [];
    $scope.transactionCategories = [];
    $scope.repeatTypes = [];
    $scope.selected = {
        dateStart: new Date(),
        repeatValue: 1
    };

    $scope.getAccounts = function() {
        accountService.getAccounts().then(function(result) {
            $scope.accounts = result.data.response;
            $scope.selected.account = $scope.accounts[0];
        })
    };

    $scope.getTransactionTypes = function() {
        accountService.getTransactionTypes().then(function(result) {
            $scope.transactionTypes = result.data.response;
            $scope.selected.type = $scope.transactionTypes[0];
        })
    };

    $scope.getTransactionCategories = function() {
        accountService.getTransactionCategories().then(function(result) {
            $scope.transactionCategories = result.data.response;
            $scope.selected.category = $scope.transactionCategories[0];
        })
    };

    $scope.getRepeatTypes = function() {
        accountService.getRepeatTypes().then(function(result) {
            $scope.repeatTypes = result.data.response;
            $scope.selected.repeatType = $scope.repeatTypes[2];
        })
    };

    $scope.submit = function() {
        $uibModalInstance.close($scope.selected);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});