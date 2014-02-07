function StaffNaveCtrl($scope, Restangular) {
    $scope.tweetMode = false;

    $scope.tweeterMode = function() {
        if($scope.tweetMode)  {
            $scope.tweetMode = false;
        }
        else {
            $scope.tweetMode =  true;
        };
    };
}