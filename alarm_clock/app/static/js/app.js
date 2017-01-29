'use strict';
var app = angular.module('app', ['ngWebsocket', 'ngRoute', 'ui.router', 'ui.bootstrap'])
    .config(['$urlRouterProvider','$stateProvider', function($urlRouterProvider, $stateProvider) {
        $urlRouterProvider.otherwise('/');
        $stateProvider
            .state('home', {
                url:'/',
                templateUrl: '/partials/home.html',
                controller: 'HomeCtrl',
                params: {
                    notification: null
                }
            })
            .state('newAlarm', {
                url:'/newAlarm',
                templateUrl: '/partials/new-alarm.html',
                controller: 'NewAlarmCtrl'
            });
    }])
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
                        scope.UI.addAlarmToUI(data);
                    });
                }
                addAlarm(data);                
          }).$on('alarmDeleted', function (data) {
                function deleteAlarm(data) {
                    var scope = angular.element(document.getElementById("alarm-widget")).scope();
                    scope.$apply(function () {
                        scope.UI.deleteAlarmFromUI(data);
                    });
                }
                deleteAlarm(data);
          }).$on('alarmUpdated', function (data) {
                function toggleAlarmUI(data) {
                    var scope = angular.element(document.getElementById("alarm-widget")).scope();
                    scope.$apply(function () {
                        scope.UI.toggleAlarmUI(data);
                    });
                }
                toggleAlarmUI(data);
          })
          .$on('$close', function () {
            console.log('WS Closed.');
          });
    });