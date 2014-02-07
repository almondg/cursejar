'use strict';
/*jshint multistr: true */

angular.module('toungeBitersApp', [
	'ngCookies',
	'ngResource',
	'ngSanitize',
	'ngRoute'
])
	.config(function ($routeProvider) {
		$routeProvider
			.when('/', { templateUrl: 'static/views/main.html', controller: 'MainCtrl' })
			.when('/jar/create', { templateUrl: 'static/views/create-jar.html', controller: 'CreateJar' })
			.when('/jar/:jarId', { templateUrl: 'static/views/view-jar.html', controller: 'ViewJar' })
			.when('/jar/:jarId/extended', { templateUrl: 'static/views/view-jar.html', controller: 'ViewJar' })
			.when('/dashboard', { templateUrl: 'static/views/dashboard.html', controller: 'Dashboard' })
			.otherwise({
				redirectTo: '/'
			});
	}).
	directive('autoCompleteInputFieldIdiot', ['$filter', '$timeout', function($filter, $timeout){
		return {
			restrict: 'C',
			// priority: 1,
			// terminal: true,
			scope: {
				list: '=',
				selectedItemsList: '=',
				ngModel: '=',
				placeholder: '@'
			},
			replace: true,
			// transclude: true,
			// compile: function(tElement, tAttrs, function transclude(function(scope, cloneLinkingFn){ return function linking(scope, elm, attrs){}})),
			link: function($scope) {
				for (var i = 0; i < $scope.list.length; i++) {
					$scope.list[i].selected = false;
				}

				function updateSelectedItem() {
					$scope.hoveredItem = $filter('filter')($scope.list, $scope.inputText);
					if ($scope.hoveredItem.length) {
						$scope.hoveredItem = $scope.hoveredItem[0];
					} else {
						$scope.hoveredItem = null;
					}
				}

				$scope.$watch('inputText', updateSelectedItem);
				$scope.$watch('isFocused', updateSelectedItem);

				$scope.onListItemClick = function(listItem) {
					if (listItem) {
						listItem.selected = true;
						$scope.selectedItemsList.push(listItem);
						$scope.inputText = '';
					}
				};

				$scope.onKeydown = function (e) {
					if (e.keyCode === 13) {
						if ($scope.hoveredItem) {
							$scope.onListItemClick($scope.hoveredItem);
						}
					}
				};

				$scope.onSelectedListItemClick = function(listItem) {
					listItem.selected = false;
					$scope.selectedItemsList.splice($scope.selectedItemsList.indexOf(listItem), 1);
				};

				$scope.onBlur = function () {
					$timeout(function () {
						$scope.isFocused = false;
					}, 100);
				};
			},
			template: '<div> \
				<div class="row"> \
					<div class="col-sm-9"><input ng-model="inputText" placeholder="{{placeholder}}" ng-focus="isFocused = true" ng-blur="onBlur()" ng-keydown="onKeydown($event)"></div> \
					<div class="col-sm-3"><a href="#" ng-click="$event.preventDefault(); onListItemClick(hoveredItem)">Add</a></div> \
				</div> \
				<div class="row"> \
					<div class="col-sm-9 list-items-container"> \
						<ul class="list-items" ng-show="isFocused"> \
							<li ng-repeat="listItem in list | filter: inputText | filter: {selected: false}" \
								ng-click="onListItemClick(listItem);" \
								ng-class="{selected: hoveredItem === listItem}"> \
								{{listItem.label}} \
							</li> \
						</ul> \
					</div> \
					<div class="col-sm-9 selected-items-container"> \
						<ul class="selected-items"> \
							<li ng-repeat="listItem in selectedItemsList" ng-click="onSelectedListItemClick(listItem);"> \
								<span>{{listItem.label}}</span> \
								<i class="pull-right glyphicon glyphicon-remove"></i> \
							</li> \
						</ul> \
					</div> \
				</div> \
			</div>'
		};
	}]);