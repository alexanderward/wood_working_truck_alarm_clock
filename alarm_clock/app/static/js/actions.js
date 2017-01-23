var UI = {
    showAlarm: function () {
        $('#clock').fadeOut(function(){
           $('#alarm-video').fadeIn();
        });
    },
    hideAlarm: function(){
        $('#alarm-video').fadeOut(function(){
            $('#clock').fadeIn();
        });
    }
};


var actions = {
    startAlarm: function(obj) {
        console.log('startAlarm:' + obj.video.url);
        UI.showAlarm();
        player.loadVideoByUrl(obj.video.url);
    },
    stopAlarm: function(obj) {
        console.log('stopAlarm');
        UI.hideAlarm();
        player.stopVideo();
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

var conductAction = function (event ,data) {
    if (event){
        if (event == 'startAlarm'){
            actions.startAlarm(data);
        }else if(event == 'stopAlarm'){
            actions.stopAlarm(data);
        }else if(event == 'alarmCreated'){
            actions.alarmCreated(data);
        }else if(event == 'userConnected'){
            actions.userConnected(data);
        }else if(event == 'userDisconnected'){
            actions.userDisconnected(data);
        }else{
            console.log('Unknown event: ' + event);
        }
    }

};