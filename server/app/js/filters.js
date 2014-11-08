njOnTime.filter('timeFromServer', function() {
	return function(input) {
		if (!input) { return input; }
		input = String(input);
		return +input.slice(0, 2) + ':' + input.slice(2);
	}
});