
app.controller('EditVideoCtrl', function($scope, VideoService){
    // Form
    $scope.newalarmForm = {
        name: null,
        video: null        
    };
    $scope.updateForm = {
        video: null        
    };

    VideoService.getVideos()
        .then(function(data) {
                $scope.vidoes = data;
            }, function(error) {
                   console.log(error)
        });

});



