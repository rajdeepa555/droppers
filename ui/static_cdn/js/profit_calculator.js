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
		var values = {"source_price":$scope.source_price,"perc_margin":$scope.perc_margin,"ebay_fvf":$scope.ebay_fvf,"fixed_margin":$scope.fixed_margin}
		$scope.flag = true;
		$http({
                    method: "post",
                    url: "http://34.232.210.211:3001/get-ebay-profit/",
                    data: values
                }).then(function(response) {
		        $scope.result_paypal_fee = "$"+response.data['paypal_fees'];
		        $scope.result_ebay_fvf = "$"+response.data["ebay_final_value_fee"];
		        $scope.result_fixed_margin = "$"+response.data["fixed_margin"];
		        $scope.result_source_price = "$"+response.data["source_price"];
			    $scope.result_selling_price = "$"+response.data["selling_price"];
			    $scope.result_ebay_listing_fee = "$"+response.data["ebay_listing_fee"];
			    $scope.result_expected_profit = "$"+response.data["expected_profit"]
				$scope.flag = true;

				console.log($scope.flag)
		    });

	}  

$scope.get_calculator = function()
	{
		$http.get("http://34.232.210.211:3001/get-ebay-profit/")
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

