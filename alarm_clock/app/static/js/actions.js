var UI = {
    showAlarm: function () {
        $('#clock').hide();
        $('#alarm-video').show();
    },
    hideAlarm: function(){
        $('#alarm-video').hide();
        $('#clock').show();
    }
};


var actions = {
    startAlarm: function(obj) {
        console.log('startAlarm:');
        UI.showAlarm();
        player.loadVideoByUrl(obj.video_url);
    },
    stopAlarm: function(obj) {
        console.log('stopAlarm: ' + obj);
        UI.hideAlarm();
    },
    alarmCreated: function(obj) {
        console.log('alarmCreated: ' + obj);
    },
    userConnected: function(obj) {
        console.log('userConnected: ' + obj);
    },
    userDisconnected: function(obj) {
        console.log('userDisconnected: ' + obj);
    }
};

var conductAction = function (message) {
    var event = message.event;
    if (event){
        if (event == 'startAlarm'){
            actions.startAlarm(message.alarm);
        }else if(event == 'stopAlarm'){
            actions.stopAlarm(message.alarm);
        }else if(event == 'alarmCreated'){
            actions.alarmCreated(message);
        }else if(event == 'userConnected'){
            actions.userConnected(message.message);
        }else if(event == 'userDisconnected'){
            actions.userDisconnected(message.message);
        }else{
            console.log('Unknown event: ' + event);
        }
    }

};