var profitCalculatorApp = angular.module('profitCalculatorApp', []);
profitCalculatorApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});
profitCalculatorApp.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);

    for (var i=0; i<total; i++) {
      input.push(i);
    }

    return input;
  };
});
profitCalculatorApp.controller('profitCalculatorCtrl', function($scope,$http,$timeout) {
    $scope.source_price = "";
    $scope.perc_margin = "";
	$scope.ebay_fvf = "";
    $scope.fixed_margin = "";
    $scope.result_source_price = "";
    $scope.result_paypal_fee = "";
	$scope.result_ebay_fvf = "";
    $scope.result_fixed_margin = "";
    $scope.result_selling_price = "";
    $scope.result_ebay_listing_fee = ""
    $scope.result_expected_profit = ""
    $scope.flag = false;

    $scope.calculateProfit = function()
	{
		 var csrftoken = getCookie('csrftoken');
        var headers = {};
        headers["X-CSRFToken"] = csrftoken;
		var values = {"source_price":$scope.source_price,"perc_margin":$scope.perc_margin,"ebay_fvf":$scope.ebay_fvf,"fixed_margin":$scope.fixed_margin}
		$scope.flag = true;
		$http({
                    method: "post",
                    url: "/get-ebay-profit/",
					data: values,
					headers:headers
                }).then(function(response) {
		        $scope.result_paypal_fee = "$"+response.data['paypal_fees'];
		        $scope.result_ebay_fvf = "$"+response.data["ebay_final_value_fee"];
		        $scope.result_fixed_margin = "$"+response.data["fixed_margin"];
		        $scope.result_source_price = "$"+response.data["source_price"];
			    $scope.result_selling_price = "$"+response.data["selling_price"];
			    $scope.result_ebay_listing_fee = "$"+response.data["ebay_listing_fee"];
			    $scope.result_expected_profit = "$"+response.data["expected_profit"]
				$scope.flag = true;

				// console.log($scope.flag)
		    });

	}  

    // $scope.calculateProfit = function(){
    //     var values = {"source_price":$scope.source_price,"perc_margin":$scope.perc_margin,"ebay_fvf":$scope.ebay_fvf,"fixed_margin":$scope.fixed_margin}
    //     var csrftoken = getCookie('csrftoken');
    //     var headers = {};
    //     headers["X-CSRFToken"] = csrftoken;

    //     // http request start
    //     $http({url: "/get-ebay-profit/", method: "post",data: values,headers:headers})
    //     .success(function (data, status, headers, config , response) {
	// 		console.log("data submitted successfull",values);
	// 	        $scope.result_paypal_fee = "$"+response.data['paypal_fees'];
	// 	        $scope.result_ebay_fvf = "$"+response.data["ebay_final_value_fee"];
	// 	        $scope.result_fixed_margin = "$"+response.data["fixed_margin"];
	// 	        $scope.result_source_price = "$"+response.data["source_price"];
	// 		    $scope.result_selling_price = "$"+response.data["selling_price"];
	// 		    $scope.result_ebay_listing_fee = "$"+response.data["ebay_listing_fee"];
	// 		    $scope.result_expected_profit = "$"+response.data["expected_profit"]
	// 			$scope.flag = true;
    //     })
    //     .error(function (data, status, headers, config , response) {
    //         console.log(error);
	// 	});
		
    // }


$scope.get_calculator = function()
	{
		$http.get("/get-ebay-profit/")
		    .then(function(response) {
		        $scope.perc_margin = response.data['perc_margin'];
		        $scope.ebay_fvf = response.data["ebay_fvf"];
		        $scope.fixed_margin = response.data["fixed_margin"];
		     	console.log("blaaa response",response.data)
		     	console.log("blaaa",$scope.perc_margin)

		    });
		     

	}
$scope.get_calculator();
 

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
