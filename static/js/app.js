'use strict';

function $apiRoot() {
    return $("#linkApiRoot").attr("href");
}

// Declare app level module which depends on views, and components
var app = angular.module('myCashManager', [
  'ngRoute',
  'xeditable',
  'myCashManager.dash',
  'myCashManager.account',
  'myCashManager.version',
  'myCashManager.commonServices',
  'myCashManager.accountServices',
  'myCashManager.category',
  'myCashManager.cycles'
]).config(['$routeProvider', function($routeProvider) {
  $routeProvider.otherwise({redirectTo: '/dash'});
}]).directive('classOnActiveLink', [function() {
  return {
    link: function(scope, element, attrs) {

      var anchorLink = element.children()[0].getAttribute('ng-href') || element.children()[0].getAttribute('href');
      anchorLink = anchorLink.replace(/^#/, '');
      //anchorLink = anchorLink.substring(0, anchorLink.indexOf('/'));
      console.log(anchorLink);

      scope.$on("$routeChangeSuccess", function (event, current) {
        if (current.$$route !== undefined && current.$$route.originalPath.startsWith(anchorLink)) {
          element.addClass(attrs.classOnActiveLink);
        } else {
          element.removeClass(attrs.classOnActiveLink);
        }
      });

    }
  };
}]);

app.run(function(editableOptions) {
    editableOptions.theme = 'bs3';
});