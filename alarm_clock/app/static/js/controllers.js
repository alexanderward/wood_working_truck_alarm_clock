
app.controller('Configure', function($scope, AlarmService, VideoService){
	var convertTime = function (time) {
		var tmp_time;
		tmp_time = convertTo12Hour(time);
		return tmp_time.split(' ');
	};
	var find_alarm_in_array = function(alarm){
		var index;
		$scope.alarms.forEach(function (value, i) {
			if (value.id == alarm.id){
				index = i;
				return true;
			}
		});
		return index;
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
	$scope.toggleAlarmUI = function(alarm){
		if (alarm.last_edited_by != threadID){
			var i = find_alarm_in_array(alarm);
			if (i === parseInt(i)){
				$scope.alarms[i].enabled = !$scope.alarms[i].enabled;
			}
		}
	};

	$scope.addAlarm = function(){
		console.log('New Alarm');
	};
	$scope.addAlarmToUI = function(alarm){
		[alarm.time, alarm.timeOfDay] = convertTime(alarm.time);
		$scope.alarms.push(alarm);
	};

	$scope.deleteAlarmFromUI = function(alarm){
		var i = find_alarm_in_array(alarm);
		if (i === parseInt(i)){
			$scope.alarms.splice(i, 1);
		}
	};

	$scope.deleteAlarm = function(index){
		var alarm = $scope.alarms[index];
		AlarmService.deleteAlarm(alarm).then(function(data) {
				$scope.deleteAlarmFromUI(alarm);
            }, function(error) {
			    console.log(error);
			    alert(error);
        });
	}

});