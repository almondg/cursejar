'use strict';

function CreateJar($scope, $location) {
	$scope.friends = [
		{
			label: 'Venessa Williams',
			avatarURL: '/static/images/avatars/avatar1.jpg'
		},
		{
			label: 'Adi Klag',
			avatarURL: '/static/images/avatars/avatar2.jpg'
		},
		{
			label: 'Yael Shterenberg',
			avatarURL: '/static/images/avatars/avatar4.jpg'
		},
		{
			label: 'Benjamin Crates',
			avatarURL: '/static/images/avatars/avatar5.jpg'
		}
	];

	$scope.selectedFriends = [];

	$scope.selectedWords = [];

	$scope.onAddWord = function () {
		if ($scope.inputWord) {
			$scope.selectedWords.push($scope.inputWord);
			$scope.inputWord = '';
		}
	};

	$scope.onSelectedWordsListItemClick = function (listItem) {
		$scope.selectedWords.splice($scope.selectedWords.indexOf(listItem), 1);
	};

	$scope.onKeydown = function(e) {
		if (e.keyCode === 13) {
			if ($scope.selectedWords.indexOf($scope.inputWord) === -1) {
				$scope.onAddWord();
			}
		}
	};

	$scope.onGo = function (e) {
		e.preventDefault();
		$location.path('jar/1');
		console.log('go!');
	};
}

CreateJar.$inject = ['$scope', '$location'];