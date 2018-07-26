var multiEbayAccountApp = angular.module('multiEbayAccountApp', []);
multiEbayAccountApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

multiEbayAccountApp.controller('multiEbayAccountCtrl', function($scope,$http) {

    $scope.added_to_pending = function(){
        alert("ebay multi account ctrl working");
    }

    $scope.get_active_seller = function()
    {
    $http.get("/activate-seller-account/")
    .then(function(response) {
        $scope.active_seller = response.data["sellers"];
        console.log("Activeeeee sellers",$scope.active_seller);
    });
    }

$scope.get_active_seller();
$scope.delete_seller = function(seller_id,seller_status)
    {
        var seller_status_delete = seller_status;
        console.log("now active",seller_status_delete);
        if (seller_status == true)
        {
            alert("Can't Delete Active seller.");
        }
        else{
        var confirm_delete = confirm("Do You Really Want To Delete This?");
        if(confirm_delete == true){
        var csrftoken = getCookie('csrftoken');
        var headers = {};
        headers["X-CSRFToken"] = csrftoken;
        headers["Content-Type"] = "application/x-www-form-urlencoded";
        var delete_id = seller_id;
        $http({url: "/delete-seller/", method: "post",data:delete_id,headers:headers})
        .success(function (data, status,config,headers) {
        console.log("data deleted successfull",delete_id);
            // $scope.ebay_seller_reports();
        window.location.reload();

        })
        .error(function (data, status,config,headers) {
            console.log("error");
        });
        return true;
        }
        else{
            // alert("Not deleted.");
            return false;
        }
        }//else of first if
    }

$scope.is_active_pk = function(value,is_eligible_for_ebay_updates){
    console.log(is_eligible_for_ebay_updates);
    if (is_eligible_for_ebay_updates == false)
    {
        alert("Please update price formula first by clicking the button. Only then you can activate seller account.")
        $scope.get_active_seller();

        // return true;
    }
    else
    {
	var csrftoken = getCookie('csrftoken');
    var headers = {};
    headers["X-CSRFToken"] = csrftoken;
    $scope.pk = value;
    var pk_value = $scope.pk
            $http({url: "/activate-seller-account/", method: "post",data: pk_value,headers:headers})
        .success(function (data, status,config,headers) {
            console.log("data submitted successfull",pk_value);
            $scope.get_active_seller();
        })
        .error(function (data, status,config,headers) {
            console.log(error);
        });
    }

}

   $scope.is_eligible = function(pk){
        // alert("hi");

        var is_eligible_pk = pk;
        console.log(is_eligible_pk);

        $http({url: "/price-formula/"+"?pk="+is_eligible_pk, method: "get",data: {"pk":is_eligible_pk}})
        .success(function (data, status,config,headers) {
            console.log("data submitted successfull",is_eligible_pk);
        })
        .error(function (data, status,config,headers) {
            console.log(error);
        });

    }


    $scope.is_update = function(seller_name,update){
        console.log(seller_name,update);

        var this_data = {"seller_name":seller_name,"is_update":update};

	    var csrftoken = getCookie('csrftoken');
        var headers = {};
        headers["X-CSRFToken"] = csrftoken;
        $http({url: "/set-update-status/", method: "post",data:this_data,headers:headers})
        .success(function (data, status,config,headers) {
            console.log("data sumbitted successfull",this_data);
            // $scope.get_active_seller();
        })
        .error(function (data, status,config,headers) {
            console.log("error while submitting",this_data);
        });


    }

    $scope.is_update_true = function(name,val_true){
        var this_data = {"seller_name":name,"is_update":val_true};
        console.log(this_data);
	    var csrftoken = getCookie('csrftoken');
        var headers = {};
        headers["X-CSRFToken"] = csrftoken;
        $http({url: "/set-update-status/", method: "post",data:this_data,headers:headers})
        .success(function (data, status,config,headers) {
            console.log("data sumbitted successfull",this_data);
            $scope.get_active_seller();
        })
        .error(function (data, status,config,headers) {
            console.log("error while submitting",this_data);
        });

    }


    $scope.is_update_false = function(name,val_false){
        var this_data = {"seller_name":name,"is_update":val_false};
        console.log(this_data);
	    var csrftoken = getCookie('csrftoken');
        var headers = {};
        headers["X-CSRFToken"] = csrftoken;
        $http({url: "/set-update-status/", method: "post",data:this_data,headers:headers})
        .success(function (data, status,config,headers) {
            console.log("data sumbitted successfull",this_data);
            $scope.get_active_seller();
        })
        .error(function (data, status,config,headers) {
            console.log("error while submitting",this_data);
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
