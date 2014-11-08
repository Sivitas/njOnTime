njOnTime.controller('departureCtrl', ['$scope', 'Const',
function($scope, Const) {
	var departureScope = $scope.departureScope = {};

	departureScope.departingTrains = [
		{
			estimatedDepartureTime: '0950',
			departureTime: '0940',
			destination: 'New York Penn Station',
			track: '1',
			line: 'Northeast Corridor',
			lineCode: 'nec', // convert to lower case
			train: '7878',
			status: 'on time',
			details: []
		},
		{
			estimatedDepartureTime: '0930',
			departureTime: '0940',
			destination: 'New York Penn Station',
			track: '13',
			line: 'Northeast Corridor',
			lineCode: 'nec', // convert to lower case
			train: '7878',
			status: 'meh',
			details: []
		},
		{
			estimatedDepartureTime: '0930',
			departureTime: '0930',
			destination: 'New York Penn Station',
			track: null,
			line: 'Northeast Corridor',
			lineCode: 'nec', // convert to lower case
			train: '7878',
			status: 'meh',
			details: []
		}
	];
}]);