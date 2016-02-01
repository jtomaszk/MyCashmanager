/**
 * Created by jarema-user on 2016-01-30.
 */

angular.module('myCashManager.dash').controller('ModalCreateAccountCtrl',
    function ($scope, $uibModalInstance, items, accountService) {

    $scope.currencies = [];
    $scope.selected = {
        currency: '',
        accountName: ''
    };

    $scope.getCurrencies = function() {
        accountService.getCurrencies().then(function(result) {
            $scope.currencies = result.data.response;
            $scope.selected.currency = $scope.currencies[0];
        })
    };

    $scope.submit = function() {
        $uibModalInstance.close($scope.selected);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});