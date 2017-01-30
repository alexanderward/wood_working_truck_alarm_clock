
app.controller('HomeCtrl', function($scope, AlarmService, $stateParams, $state){
	if ($stateParams.notification){
		notificationPopup($stateParams.notification.title, $stateParams.notification.message, $stateParams.notification.status, $stateParams.notification.icon);		
	}

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

	$('#action-Btn').html('<a class="btn btn-primary" href="#!/newAlarm"><i class="fa fa-plus"></i> Add</a>');


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

	$scope.editAlarm = function(event, alarm){
		$state.go('editAlarm', {alarm: alarm});
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
        });

    };

	$scope.deleteAlarm = function(index){
		var alarm = $scope.alarms[index];
		AlarmService.deleteAlarm(alarm).then(function(data) {
				$scope.UI.deleteAlarmFromUI(alarm);
            }, function(error) {
			    console.log(error);
        });
	};
	$scope.UI = {
		toggleAlarmUI : function(alarm){
			if (alarm.last_edited_by != threadID){
				var i = find_alarm_in_array(alarm);
				if (i === parseInt(i)){
					$scope.alarms[i].enabled = !$scope.alarms[i].enabled;
				}
			}
		},
		addAlarmToUI : function(alarm){
			if (alarm.last_edited_by != threadID) {
				[alarm.time, alarm.timeOfDay] = convertTime(alarm.time);
				$scope.alarms.push(alarm);
				notificationPopup("Alarm Created!", 'Successfully created new Alarm: ' + alarm.name, "success", "fa fa-check");
			}
		},
		deleteAlarmFromUI : function(alarm){
			var i = find_alarm_in_array(alarm);
			if (i === parseInt(i)) {
				$scope.alarms.splice(i, 1);
				notificationPopup("Deleted Alarm", "Successfully Deleted Alarm: " + alarm.name, "success", "fa fa-trash");
			}
		}
	};




});