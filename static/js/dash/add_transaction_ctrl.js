/**
 * Created by jarema-user on 2016-01-30.
 */

angular.module('myCashManager.dash').controller('ModalAddTransactionCtrl',
    function ($scope, $uibModalInstance, accountService, accountId) {

    $scope.transactionTypes = [];
    $scope.transactionCategories = [];
    $scope.selected = {
        accountId: accountId,
        type: '',
        category: '',
        date: new Date(),
        value: '',
        comment: ''
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
    };

    $scope.submit = function() {
        $uibModalInstance.close($scope.selected);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});