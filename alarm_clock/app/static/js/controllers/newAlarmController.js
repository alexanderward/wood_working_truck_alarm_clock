app.controller('NewAlarmCtrl', function($scope, VideoService, AlarmService, $log, $state){
    // Configurations
    $scope.title = "Create Alarm";
    $('#action-Btn').html('<a class="btn btn-primary" href="#!/"><i class="fa fa-home"></i> Home</a>');

    var convertTimeToString = function(time_){
        return time_.getHours() +":"+ time_.getMinutes() + ":" + time_.getSeconds();
    };

    $scope.hstep = 1;
    $scope.mstep = 1;
    $scope.ismeridian = true;    
    $scope.alarmTime = new Date();
    $scope.form = {
        name: null,
        time: convertTimeToString($scope.alarmTime),
        video: null,
        flashingLights: true,
        monday:false,
        tuesday:false,
        wednesday:false,
        thursday:false,
        friday:false,
        saturday:false,
        sunday:false,
        enabled:true
    };

    VideoService.getVideos()
        .then(function(data) {
                $scope.baseDropDownVideos = data;
            }, function(error) {
                   console.log(error)
        });
    
    

    $scope.submit = function() {
        AlarmService.createAlarm($scope.form)
        .then(function(data) {            
            console.log('Successfully created new Alarm: ' + data.name);
            $state.go('home', {notification: {
                                title: 'Alarm Created!',
                                message: 'Successfully created new Alarm: ' + data.name,
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
            notificationPopup("Error creating Alarm: " + $scope.form.name, error, 'error', "fa fa-exclamation-circle");

        });
    };

    $scope.changed = function () {
        $log.log('Time changed to: ' + $scope.alarmTime);
        $scope.form.time = convertTimeToString($scope.alarmTime);
        console.log($scope.form);
    };

});