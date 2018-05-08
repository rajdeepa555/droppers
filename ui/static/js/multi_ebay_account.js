var multiEbayAccountApp = angular.module('multiEbayAccountApp', []);
multiEbayAccountApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

multiEbayAccountApp.controller('multiEbayAccountCtrl', function($scope,$http) {

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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
