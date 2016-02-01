'use strict';

angular.module('myCashManager.category', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/category', {
    templateUrl: $apiRoot() + 'category/category.html',
    controller: 'CategoryCtrl'
  });
}]).controller('CategoryCtrl', function($scope, $q, accountService) {
    $scope.list = [];

    $scope.initCategoryList = function() {
        accountService.getTransactionCategories().then(function(result) {
            $scope.list = result.data.response;
            angular.forEach($scope.list, function(i){
                i.edit = false;
                i.error = false;
            });
        });
    };

    $scope.errorStyle = function(bool) {
        if (bool) {
            return 'has-error';
        }
    };

    $scope.editShelf = function(i){
        i.edit = true;
    };

    $scope.saveShelf = function(i){
        i.edit = false;

        if (!i.name) {
            i.error = true;
            return;
        }
        i.error = false;

        var defer;
        if (i.id) {
            defer = accountService.postTransactionCategory(i)
        } else {
            defer = accountService.putTransactionCategory(i);
        }

        defer.then(function(result) {
            $scope.initCategoryList();
        });
    };

    $scope.add = function() {
        $scope.list.push({
            name: '',
            error: true,
            edit: true
        });
    }
});