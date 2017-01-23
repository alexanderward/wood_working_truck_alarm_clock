'use strict';
var app = angular.module('app', ['ngWebsocket'])
    .run(function ($websocket) {
        var ws = $websocket.$new("ws://"+window.location.hostname + ":" + sse_port + "/ws/" + sse_channel)
          .$on('$open', function () {
            console.log('Connected to WS.');
          }).$on('userConnected', function (data) {
                //noinspection JSUnresolvedVariable
                threadID = data.threadID;
            }).$on('alarmCreated', function (data) {
                function addAlarm(data) {
                    var scope = angular.element(document.getElementById("alarm-widget")).scope();
                    scope.$apply(function () {
                    scope.addAlarmToUI(data);
                    });
                }
                addAlarm(data);                
          }).$on('alarmDeleted', function (data) {
                function deleteAlarm(data) {
                    var scope = angular.element(document.getElementById("alarm-widget")).scope();
                    scope.$apply(function () {
                    scope.deleteAlarmFromUI(data);
                    });
                }
                deleteAlarm(data);
          }).$on('alarmUpdated', function (data) {
                function toggleAlarmUI(data) {
                    var scope = angular.element(document.getElementById("alarm-widget")).scope();
                    scope.$apply(function () {
                    scope.toggleAlarmUI(data);
                    });
                }
                toggleAlarmUI(data);
          })
          .$on('$close', function () {
            console.log('WS Closed.');
          });
    });