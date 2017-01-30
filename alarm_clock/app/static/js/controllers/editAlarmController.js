app.controller('EditAlarmCtrl', function($scope, VideoService, AlarmService, $log, $stateParams, $state){
    // Configurations
    $('#action-Btn').html('<a class="btn btn-primary" href="#!/"><i class="fa fa-home"></i> Home</a>');
    if ($stateParams.alarm === null){
        $state.go('home');
        return
    }


    $scope.form = $stateParams.alarm;
    $scope.hstep = 1;
    $scope.mstep = 1;
    $scope.ismeridian = true;
    $scope.alarmTime = convertStringTo24HourDate($scope.form.time, $scope.form.timeOfDay);

    var convertTimeToString = function(time_){
        return time_.getHours() +":"+ time_.getMinutes() + ":" + time_.getSeconds();
    };

    VideoService.getVideos()
        .then(function(data) {
                $scope.baseDropDownVideos = data;
            }, function(error) {
                   console.log(error)
        });
    
    

    $scope.submit = function() {
        AlarmService.updateAlarm($scope.form)
        .then(function(data) {            
            console.log('Successfully updated Alarm: ' + data.name);
            $state.go('home', {notification: {
                                title: 'Alarm Updated!',
                                message: 'Successfully updated Alarm: ' + data.name,
                                color: '#',
                                status: 'success',
                                icon: "fa fa-check"
                              }
            });
        }, function(error) {            
            if (typeof error == 'object'){
                error = JSON.stringify(error);

            }else if (error[0].includes("column name is not unique")){
                error = "Duplicate Alarm name.  Please choose another."
            }
            notificationPopup("Error updating Alarm: " + $scope.form.name, error, 'error', "fa fa-exclamation-circle");
            console.log(error)
        });
    };

    $scope.changed = function () {
        $log.log('Time changed to: ' + $scope.alarmTime);
        $scope.form.time = convertTimeToString($scope.alarmTime);
        console.log($scope.form);
    };

});