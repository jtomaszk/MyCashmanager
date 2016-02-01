/**
 * Created by jtomaszk on 29.01.16.
 */

'use strict';

angular.module('myCashManager.commonServices', [])
    .factory('appService', function() {
    return {
        apiRoot: function() {
            return $apiRoot();
        }
    }
});