var multiEbayAccountApp = angular.module('AccountSettingsApp', []);
multiEbayAccountApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

multiEbayAccountApp.controller('AccountSettingsCtrl', function($scope,$http) {

    console.log("Account-settings ctrl working");

    $scope.get_active_seller = function()
    {
    $http.get("/update-custom-stock/")
    .then(function(response) {
        $scope.all_seller = response.data;
        console.log("All sellers",$scope.all_seller);
        $scope.selectedseller= response.data[0]["sellername"];
        // console.log($scope.selectedseller);

    });
    }

    $scope.get_active_seller();


    $scope.get_seller = function(seller){
        var current_seller = seller;
        console.log(current_seller);

    }

    $scope.post_seller_details = function(pk,default_stock){
        var seller_dict = {"pk":pk,"default_stock":default_stock}
        console.log(seller_dict);

	    var csrftoken = getCookie('csrftoken');
        var headers = {};
        headers["X-CSRFToken"] = csrftoken;
        $http({url: "/update-custom-stock/", method: "post",data:seller_dict,headers:headers})
        .success(function (data, status,config,headers) {
            console.log("data sumbitted successfull",seller_dict);
            $scope.get_active_seller();
        })
        .error(function (data, status,config,headers) {
            console.log("error while submitting",seller_dict);
        });

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
