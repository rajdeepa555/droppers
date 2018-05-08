var addEbaySellerKeysetApp = angular.module('addEbaySellerKeysetApp', []);
addEbaySellerKeysetApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

addEbaySellerKeysetApp.controller('addEbaySellerKeysetCtrl', function($scope,$http,$timeout) {
    $scope.items = [{'sellername': 'false', 'appid': 'Indigo Women Top', 'devid': '$34','certid':'2','token':'1'}];
   	
	// $scope.select_all = function(){
	// 	$timeout(function(){
	// 			for(var i in $scope.items)
	// 	        {
	// 	        	$scope.items[i]["is_checked"] = true;
	// 	        }
	// 	}, 500);
	// }

	$scope.add = function(){
			keyset={}
        	keyset["sellername"]=$scope.sellername;
        	keyset["appid"]=$scope.appid;
        	keyset["devid"]=$scope.devid;
        	keyset["certid"]=$scope.certid;
        	keyset["token"]=$scope.token;

        	$scope.cfdump = "";

        	var request = $http({
                    method: "post",
                    url: "http://34.209.204.106:3004/add-ebay-keyset/",
                    // transformRequest: transformRequestAsFormPost,
                    data: keyset
                });

        	request.success(
                    function( html ) {
                        $scope.cfdump = html;
                    }
                );
        	$scope.refresh_seller_list();

	}


	$scope.submit = function()
	{
		var submit_items=[]
		for(var i in $scope.items)
		{
			if($scope.items[i]["is_checked"]==true)
			{
				$scope.submit_items=$scope.items[i]
				console.log($scope.submit_items)

			}
		}
		console.log(submit_items)
	}

	$scope.refresh_seller_list = function()
	{
		 $http.get("http://34.209.204.106:3004/get-ebay-seller-keyset/?format=json")
		    .then(function(response) {
		        $scope.items = response.data;
		        for(var i in $scope.items)
		        {
		        	$scope.items[i]["is_checked"] = false;
		        }
		    });
	}
	$scope.refresh_seller_list();
});