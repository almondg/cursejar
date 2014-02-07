'use strict';

function ViewJar($scope, $interval, $location) {
	$scope.isAfterJarCreation = ($location.path().substr(-8) !== 'extended');

	$scope.h = 'asd';
	$scope.words = ['היוש', 'ביוש'];
	$scope.countdownTimer = 23 * 60 * 60 + 59 * 60 + 3;

	$scope.friends = [
		{
			name: 'Eldad Bercovici',
			avatarURL: 'static/images/avatars/avatar3.jpg',
			money: 5,
			words: [
				{ word: 'היוש', count: 0 },
				{ word: 'ביוש', count: 5 }
			]
		},
		{
			name: 'Venessa Williams',
			avatarURL: '/static/images/avatars/avatar1.jpg',
			money: 3,
			words: [
				{ word: 'היוש', count: 1 },
				{ word: 'ביוש', count: 3 }
			]
		},
		{
			name: 'Adi Klag',
			avatarURL: '/static/images/avatars/avatar2.jpg',
			money: 2,
			words: [
				{ word: 'היוש', count: 1 },
				{ word: 'ביוש', count: 2 }
			]
		}
	];

	function updateTimer () {
		$scope.countdownTimer--;
		$scope.countdownTimerHour = Math.floor($scope.countdownTimer / 60 / 60);
		$scope.countdownTimerMin = Math.floor($scope.countdownTimer / 60) % 60;
		$scope.countdownTimerSec = $scope.countdownTimer % 60;

		if ($scope.countdownTimerHour < 10) {
			$scope.countdownTimerHour = '0' + $scope.countdownTimerHour;
		}

		if ($scope.countdownTimerMin < 10) {
			$scope.countdownTimerMin = '0' + $scope.countdownTimerMin;
		}

		if ($scope.countdownTimerSec < 10) {
			$scope.countdownTimerSec = '0' + $scope.countdownTimerSec;
		}
	}

	$scope.total = 10;

	updateTimer();

	$interval(updateTimer, 1000);
}

ViewJar.$inject = ['$scope', '$interval', '$location'];