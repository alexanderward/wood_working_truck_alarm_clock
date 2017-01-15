var tag = document.createElement('script');
var iframeId = 'alarm-video';
tag.id = 'iframe-demo';
tag.src = 'https://www.youtube.com/iframe_api';
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player(iframeId, {
        playerVars: { 'autoplay': 1, 'controls': 0 },
        events: {
          'onReady': onPlayerReady,
          'onStateChange': onPlayerStateChange
        }
    });
}
function onPlayerReady(event) {
    console.log('YouTube Player ready');
}
function onPlayerStateChange(event) {
    if(event.data === 0) {
        UI.hideAlarm();
    }
}