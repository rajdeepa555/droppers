var baseApp = angular.module('baseApp', []);
baseApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

baseApp.controller('baseCtrl', function($scope,$http) {
console.log("base app running");
    $scope.added_to_pending = function(){
        alert("ebay multi account ctrl working");
    }

    $http.get("/activate-seller-account/")
    .then(function(response) {
        $scope.active_seller = response.data["sellers"];
        console.log("Active sellers",$scope.active_seller);
    });
    
$scope.is_active_pk = function(value){

	var csrftoken = getCookie('csrftoken');
    var headers = {};
    headers["X-CSRFToken"] = csrftoken;
    $scope.pk = value;
    var pk_value = $scope.pk
            $http({url: "/activate-seller-account/", method: "post",data: pk_value,headers:headers})
        .success(function (data, status,config,headers) {
            console.log("data submitted successfull",pk_value);
        })
        .error(function (data, status,config,headers) {
            console.log(error);
        });
    // var r = confirm("You are activating another seller account. Are you sure?");
    // if (r == true) {
    //     $http({url: "/activate-seller-account/", method: "post",data: pk_value,headers:headers})
    //     .success(function (data, status,config,headers) {
    //         console.log("data submitted successfull",pk_value);
    //     })
    //     .error(function (data, status,config,headers) {
    //         console.log(error);
    //     });
    // }
    // else {
    //     txt = "You pressed Cancel!";
    // }

}

});

