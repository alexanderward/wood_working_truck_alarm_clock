
app.controller('EditVideoCtrl', function($scope, VideoService){
    $scope.safeApply = function(fn) {
        var phase = this.$root.$$phase;
        if(phase == '$apply' || phase == '$digest') {
            if(fn && (typeof(fn) === 'function')) {
                fn();
            }
        } else {
            this.$apply(fn);
        }
    };

    var updateBaseViewVideoDropDown = function(controllerElementID) {
        var scope = angular.element(document.getElementById(controllerElementID)).scope();
        $scope.safeApply(function () {
            scope.baseDropDownVideos = $scope.dropDownVideos;
            scope.form.video = null;
        });
    };

    var nullUpdateFormObject = function () {
        $scope.updateForm = {
            id: null,
            name: null,
            url: null
        };
    };

    var nullCreateFormObject = function () {
        $scope.createForm = {
                name: null,
                url: null
        };
    };

    var resetUpdateForm = function(){
        nullUpdateFormObject();
        $scope.formUpdateForm.$setPristine();
    };

    var resetCreateForm = function(){
        nullCreateFormObject();
        $scope.formCreateForm.$setPristine();
        $scope.formCreateForm.$setValidity();
        $scope.formCreateForm.$setUntouched();
    };
    var setVideoDropDownValues = function(videoObject, callback){
        VideoService.getVideos()
        .then(function(data) {
                $scope.dropDownVideos = data;
                if (typeof videoObject !== "undefined"){
                    $scope.dropdownVideo = _.find($scope.dropDownVideos, function(item) {
                        if (item.id == videoObject.id){
                            return item.id;
                        }
                    });
                    if (typeof callback !== "undefined")
                        callback();
                }
            }, function(error) {
                console.log(error)
        });

    };
    $scope.updateFormDropDownWatcher = function(alarm){
        if (typeof alarm !== "undefined"){
            $scope.updateForm.name = alarm.name;
            $scope.updateForm.url = alarm.url;
            $scope.updateForm.id = alarm.id;
        }
    };

    setVideoDropDownValues();
    nullCreateFormObject();
    nullUpdateFormObject();
    $scope.dropDownVideo = null;

    $scope.preview = function(url){
        window.open(url,'_blank');
    };
    $scope.save = function(video, mode){
        if (mode == 'update'){
            VideoService.updateVideo(video).then(function(data) {
                notificationPopup("Video Updated!", "Successfully updated video: " + data.name, 'success', "fa fa-check");
                setVideoDropDownValues(data, function(){
                    // resetUpdateForm();
                    updateBaseViewVideoDropDown("newAlarm");
                 });
            }, function(error) {
                   console.log(error);
                   notificationPopup("Error updating Video.", error, 'error', "fa fa-exclamation-circle");
        });
        }else if (mode == 'create'){
            VideoService.createVideo(video).then(function(data) {
                notificationPopup("Video Created!", "Successfully created video: " + data.name, 'success', "fa fa-check");
                setVideoDropDownValues(data, function(){
                    resetCreateForm();
                    updateBaseViewVideoDropDown("newAlarm");
                 });
            }, function(error) {
                   console.log(error);
                    if (error[0].includes("column name is not unique")){
                        error = "Duplicate Video name.  Please choose another."
                    }
                   notificationPopup("Error creating Video.", error, 'error', "fa fa-exclamation-circle");
        });
        }
    };
    $scope.delete = function(video){
        VideoService.deleteVideo(video).then(function(data) {
                notificationPopup("Video Deleted!", "Successfully deleted video: " + data.name, 'success', "fa fa-trash");
                setVideoDropDownValues(data, function(){
                    resetUpdateForm();
                    updateBaseViewVideoDropDown("newAlarm");
                 });
            }, function(error) {
                   console.log(error);
                   notificationPopup("Error deleting Video.", error, 'error', "fa fa-exclamation-circle");
        });
        
    };

});



