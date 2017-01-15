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

    function updateClock() {
        var d = new Date();
        var s = "";
        s += (10 > d.getHours() ? "0" : "") + d.getHours() + ":";
        s += (10 > d.getMinutes() ? "0" : "") + d.getMinutes();
        textNode.data = s;
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