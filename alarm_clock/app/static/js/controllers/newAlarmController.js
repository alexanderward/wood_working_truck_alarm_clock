
app.controller('NewAlarmCtrl', function($scope, VideoService, $log){
    // Configurations
    $('#action-Btn').html('<a class="btn btn-primary" href="#!/"><i class="fa fa-home"></i> Home</a>');
    $scope.hstep = 1;
    $scope.mstep = 1;
    $scope.ismeridian = true;    

    // Form
    $scope.form = {
        name: null,
        alarmTime:  new Date(),
        video: null,
        flashingLights: true,
        repeatDays: {
            monday:false,
            tuesday:false,
            wednesday:false,
            thursday:false,
            friday:false,
            saturday:false
        }
    };

    VideoService.getVideos()
        .then(function(data) {
                $scope.videos = data;
            }, function(error) {
                   console.log(error)
        });
    
    

    $scope.changed = function () {
        console.log($scope.form.alarmTime);
        $log.log('Time changed to: ' + $scope.mytime);
        console.log($scope.form);
    };
});