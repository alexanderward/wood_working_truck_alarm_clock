// $(document).ready(function() {
//     // http://flipclockjs.com/api
//     var clock = $('.clock').FlipClock({
//         clockFace: 'TwelveHourClock',
//         showSeconds: false
//     });
// });
$(document).ready(function() {
    var textElem = document.getElementById("clocktext");
    var textNode = document.createTextNode("");
    textElem.appendChild(textNode);
    var curFontSize = 24;  // Do not change

    // function calculate_am_pm(date){
    //     date
    //     return time;
    // }
    function formatDate(date) {
        var hh = date.getHours();
        var m = date.getMinutes();
        // var s = date.getSeconds();
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
    return h+":"+m+" "+dd
}

    function updateClock() {
        var d = new Date();
        textNode.data = formatDate(d);
        setTimeout(updateClock, 60000 - d.getTime() % 60000 + 100);
    }

    function updateTextSize() {
        var targetWidth = 0.9;  // Proportion of full screen width
        for (var i = 0; 3 > i; i++) {  // Iterate for better better convergence
            var newFontSize = textElem.parentNode.offsetWidth * targetWidth / textElem.offsetWidth * curFontSize;
            textElem.style.fontSize = newFontSize.toFixed(3) + "pt";
            curFontSize = newFontSize;
        }
    }

    updateClock();
    updateTextSize();
    window.addEventListener("resize", updateTextSize);
});