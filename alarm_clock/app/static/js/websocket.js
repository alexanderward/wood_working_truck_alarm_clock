var WebSocketTest = function() {
    if ("WebSocket" in window) {
        var ws = new WebSocket("ws://"+window.location.hostname + ":" + sse_port + "/ws/" + sse_channel);
        ws.onopen = function() {
            ws.send("[]Browser Connected");
        };
        ws.onmessage = function (evt) {
            var received_msg = evt.data;            
            var message = JSON.parse(received_msg);
            conductAction(message.event, message.data);
        };
        ws.onclose = function() {
            console.log('Disconnected from SSE Server');
        };
    }
};
WebSocketTest();