/**
 * Created by jarema-user on 2016-01-30.
 */

angular.module('myCashManager.dash').controller('ModalAddTransactionCtrl',
    function ($scope, $uibModalInstance, accountService, accountId) {

    $scope.transactionTypes = [];
    $scope.transactionCategories = [];
    $scope.destinationAccounts = [];
    $scope.selected = {
        accountId: accountId,
        type: null,
        category: null,
        date: new Date(),
        value: null,
        comment: null,
        destinationAccount: null
    };

    $scope.initForm = function() {
        accountService.getTransactionTypes().then(function(result) {
            $scope.transactionTypes = result.data.response;
            $scope.selected.type = $scope.transactionTypes[0];
        });
        accountService.getTransactionCategories().then(function(result) {
            $scope.transactionCategories = result.data.response;
            $scope.selected.category = $scope.transactionCategories[0];
        });
        accountService.getAccounts().then(function(result) {
            $scope.destinationAccounts = result.data.response.filter(function (item) {
                return item.id != $scope.selected.accountId;
            });
            $scope.selected.destinationAccount = $scope.destinationAccounts[0];
        });
    };

    $scope.submit = function() {
        $uibModalInstance.close($scope.selected);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});