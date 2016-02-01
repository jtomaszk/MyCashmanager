/**
 * Created by jtomaszk on 29.01.16.
 */

'use strict';

angular.module('myCashManager.accountServices', [])
.service('accountService', function ($http, $q) {
    this.getAccounts = function () {
        return $http({method: 'GET', url: '/accounts'});
    };

    this.getTransactions = function(accountId) {
        return $http({method: 'GET', url: '/transactions/' + accountId});
    };

    this.getCurrencies = function() {
        return $http({method: 'GET', url: '/currencies'});
    };

    this.putAccount = function(selected) {
        return $http.put('/account', {
            currencyId: selected.currency.id,
            accountName: selected.accountName
        });
    };

    this.putTransaction = function(selected) {
        return $http.put('/transaction', {
            accountId: selected.accountId,
            type: selected.type.enum,
            categoryId: selected.category.id,
            date: selected.date,
            value: selected.value,
            comment: selected.comment
        });
    };

    this.getTransactionTypes = function() {
        var data = {
            data: {
                response: [
                    {
                        enum: 'OUTCOME',
                        name: 'outcome'
                    }, {
                        enum: 'INCOME',
                        name: 'income'
                    }
                ]
            }
        };
        var deferred = $q.defer();
        deferred.resolve(data);
        return deferred.promise;
    };

    this.getTransactionCategories = function() {
        return $http.get('/categories');
    };

    this.putTransactionCategory = function(i) {
        return $http.put('/category', {
            category: i
        });
    };

    this.postTransactionCategory = function(i) {
        return $http.post('/category', {
            category: i
        });
    };
});