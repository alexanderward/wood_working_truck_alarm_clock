
app.controller('Configure', function($scope, AlarmService, VideoService){
	var convertTime = function (time) {
		var tmp_time;
		tmp_time = convertTo12Hour(time);
		return tmp_time.split(' ');
	};

    AlarmService.getAlarms()
        .then(function(data) {
					$.each(data, function(index, value){
						[value.time, value.timeOfDay] = convertTime(value.time)
					});
                    $scope.alarms = data;
					console.log("Retrieved Alarms");
            }, function(error) {
                   console.log(error)
        });
    VideoService.getVideos()
        .then(function(data) {
                    $scope.videos = data;
                    console.log($scope.videos);
            }, function(error) {
                   console.log(error)
        });
	
	$scope.editAlarm = function(event, team){
     	console.log(event.currentTarget, team);
    };

	$scope.toggleAlarm = function(event, alarm){
		event.stopPropagation();
		alarm.enabled = !alarm.enabled;
		var copiedAlarm = jQuery.extend(true, {}, alarm);
		copiedAlarm.time = convertTo24Hour(copiedAlarm.time);
		AlarmService.toggleAlarm(copiedAlarm).then(function(data) {
				// [alarm.time, alarm.timeOfDay] = convertTime(data.time);
				console.log("Alarm Toggled: " + alarm.name);
            }, function(error) {
                   alarm.enabled = !alarm.enabled;
			       alert(error);
        });

    };

	$scope.addAlarm = function(){
		console.log('New Alarm');
	};
	$scope.deleteAlarm = function(alarm){
		AlarmService.deleteAlarm(alarm).then(function(data) {
				$scope.alarms.splice($scope.alarms.indexOf(alarm), 1);
				console.log("Deleted Alarm: " + alarm.name);
            }, function(error) {
			    console.log(error);
			    alert(error);
        });
	}

});