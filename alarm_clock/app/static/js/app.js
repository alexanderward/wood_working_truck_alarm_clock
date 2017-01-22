'use strict';
var app = angular.module('app', ['ngWebsocket'])
    .run(function ($websocket) {
        var ws = $websocket.$new("ws://"+window.location.hostname + ":" + sse_port + "/ws/" + sse_channel)
          .$on('$open', function () {
            console.log('Connected to WS.');

            // var data = {
            //     level: 1,
            //     text: 'ngWebsocket rocks!',
            //     array: ['one', 'two', 'three'],
            //     nested: {
            //         level: 2,
            //         deeper: [{
            //             hell: 'yeah'
            //         }, {
            //             so: 'good'
            //         }]
            //     }
            // };
            //
            // ws.$emit('ping', 'hi listening websocket server') // send a message to the websocket server
            //   .$emit('pong', data);
          })
          .$on('pong', function (data) {
            console.log('The websocket server has sent the following data:');
            console.log(data);

            ws.$close();
          })
          .$on('$close', function () {
            console.log('WS Closed.');
          });
    });