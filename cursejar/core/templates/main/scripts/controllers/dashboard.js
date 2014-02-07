'use strict';

function Dashboard($scope, $interval, $location) {
	$scope.jars = [
		{
			id: '1',
			words: ['היוש', 'ביוש'],
			countdownTimer: 23 * 60 * 60 + 58 * 60 + 13,
			total: 10,
			friends: [
				{
					name: 'Eldad Bercovici',
					avatarURL: 'static/images/avatars/avatar3.jpg',
					money: 5,
					words: [
						{ word: 'היוש', count: 1 },
						{ word: 'ביוש', count: 3 }
					]
				},
				{
					name: 'Venessa Williams',
					avatarURL: '/static/images/avatars/avatar1.jpg',
					money: 3,
					words: [
						{ word: 'מגניב', count: 3 },
						{ word: 'זורם', count: 4 }
					]
				},
				{
					name: 'Adi Klag',
					avatarURL: '/static/images/avatars/avatar2.jpg',
					money: 2,
					words: [
						{ word: 'הזוי', count: 0 },
						{ word: 'פולימורפיזם', count: 5 }
					]
				}
			]
		},
		{
			id: '2',
			words: ['הזוי', 'זורם'],
			countdownTimer: 12 * 60 * 60 + 42 * 60 + 37,
			total: 10,
			friends: [
				{
					name: 'Eldad Bercovici',
					avatarURL: 'static/images/avatars/avatar3.jpg',
					money: 2,
					words: [
						{ word: 'Donkey', count: 1 },
						{ word: 'Boner', count: 3 }
					]
				},
				{
					name: 'Benjamin Crates',
					avatarURL: '/static/images/avatars/avatar5.jpg',
					money: 3,
					words: [
						{ word: 'Donkey', count: 3 },
						{ word: 'Boner', count: 4 }
					]
				},
				{
					name: 'Yael Shterenberg',
					avatarURL: '/static/images/avatars/avatar4.jpg',
					money: 0,
					words: [
						{ word: 'Donkey', count: 0 },
						{ word: 'Boner', count: 5 }
					]
				}
			]
		}
	];

	$scope.completedJars = [
		{
			id: '3',
			words: ['מגניב', 'זורם'],
			countdownTimer: 23 * 60 * 60 + 59 * 60 + 3,
			total: 17,
			winner: 'Eldad Bercovici'
		},
		{
			id: '4',
			words: ['הזוי', 'פולימורפיזם'],
			countdownTimer: 23 * 60 * 60 + 59 * 60 + 3,
			total: 83,
			winner: 'Yael Shteren...'
		},
		{
			id: '5',
			words: ['google wallet', 'square'],
			countdownTimer: 23 * 60 * 60 + 59 * 60 + 3,
			total: 42,
			winner: 'Natalie Portman'
		}
	];

	function updateTimer () {
		for (var i = 0; i < $scope.jars.length; i++) {
			$scope.jars[i].countdownTimer--;
			$scope.jars[i].countdownTimerHour = Math.floor($scope.jars[i].countdownTimer / 60 / 60);
			$scope.jars[i].countdownTimerMin = Math.floor($scope.jars[i].countdownTimer / 60) % 60;
			$scope.jars[i].countdownTimerSec = $scope.jars[i].countdownTimer % 60;

			if ($scope.jars[i].countdownTimerHour < 10) {
				$scope.jars[i].countdownTimerHour = '0' + $scope.jars[i].countdownTimerHour;
			}

			if ($scope.jars[i].countdownTimerMin < 10) {
				$scope.jars[i].countdownTimerMin = '0' + $scope.jars[i].countdownTimerMin;
			}

			if ($scope.jars[i].countdownTimerSec < 10) {
				$scope.jars[i].countdownTimerSec = '0' + $scope.jars[i].countdownTimerSec;
			}
		}
	}

	$scope.onJarClick = function(jar) {
		$location.path('jar/' + jar.id + '/extended');
	}

	$scope.isAfterJarCreation = false;

	updateTimer();
	$interval(updateTimer, 1000);
}

Dashboard.$inject = ['$scope', '$interval', '$location'];
