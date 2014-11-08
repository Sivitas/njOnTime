var njOnTime = angular.module('njOnTime', ['ngRoute']);

njOnTime.config(['$routeProvider',
function($routeProvider) {
	$routeProvider.
		when('/', { templateUrl: 'views/departure.html', controller: 'departureCtrl'}).
		otherwise({ redirectTo: '/' });
}]);