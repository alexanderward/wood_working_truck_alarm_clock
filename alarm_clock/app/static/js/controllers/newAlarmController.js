
app.controller('NewAlarmCtrl', function($scope, VideoService, $log){
    $('#action-Btn').html('<a class="btn btn-primary" href="#!/"><i class="fa fa-home"></i> Home</a>');
    VideoService.getVideos()
        .then(function(data) {
                    $scope.videos = data;
                    console.log($scope.videos);
            }, function(error) {
                   console.log(error)
        });
    
    $scope.mytime = new Date();
    $scope.hstep = 1;
    $scope.mstep = 1;
    $scope.ismeridian = true;

    $scope.changed = function () {
        $log.log('Time changed to: ' + $scope.mytime);
    };
});