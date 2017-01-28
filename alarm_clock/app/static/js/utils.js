function convertTo12Hour(date) {
        var hh, m, s;
        if (typeof date != "string"){
            hh = date.getHours();
            m = date.getMinutes();
            s = date.getSeconds();
        }else{

            [hh, m, s] = date.split(':')
            if (m.startsWith('0')){
                m = m.slice(-1);
            }
            if (hh.startsWith('0')){
                hh = hh.slice(-1);
            }

        }
        var dd = "AM";
        var h = hh;
        if (h >= 12) {
            h = hh-12;
            dd = "PM";
        }
        if (h == 0) {
            h = 12;
        }
        m = m<10?"0"+m:m;

        // s = s<10?"0"+s:s;

        /* if you want 2 digit hours: */
        h = h<10?"0"+h:h;
    return h+":"+m+" "+dd;
}
function convertTo24Hour(time, timeOfDay){
    var d, hh;
    [hh, m, s] = time.split(':');
    if (timeOfDay == 'PM'){
        hh  = hh + 12;
    }
    if (hh.startsWith('0')){
        hh = hh.slice(-1);
    }
    time = hh+":"+m;
    return time;
}

var notificationPopup = function(title, message, status, icon){
    var color;
    if (status == 'success'){
        color = '#7DC27D';
    }else if (status == 'error'){
        color = '#A90329';
    }else if (status == 'warning'){
        color = '#efe1b3';
    }else{
        color = '#d6dde7';
    }
    $.smallBox({
        title : title,
        content : message,
        color : color,
        timeout: 8000,
        icon : icon
    });

};