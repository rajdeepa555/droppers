var myEbayItemApp = angular.module('myEbayItemApp', []);
myEbayItemApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

myEbayItemApp.controller('myEbayItemCtrl', function($scope,$http,$timeout) {
    $scope.items = [{'ebay_id': '12345','photo':'http://thumbs.ebaystatic.com/pict/2632885307696464_1.jpg', 'product_name': 'Indigo Women Top', 'custom_label':'3f543f', 'price': '$34','quantity':'2','no_of_times_sold':'1','date_of_listing':'2017-10-10','is_checked':false}];

    $scope.start_search = function()
	{
		alert($scope.keyword);
	}    
	$scope.select_all = function(){
		$timeout(function(){
				for(var i in $scope.items)
		        {
		        	$scope.items[i]["is_checked"] = true;
		        }
		}, 500);
		// $scope.$apply();
	}
	$scope.submit = function()
	{
		var submit_items=[]
		for(var i in $scope.items)
		{
			if($scope.items[i]["is_checked"]==true)
			{
				submit_items.push($scope.items[i])
				console.log($scope.items[i]["is_checked"])

			}
		}
		console.log(submit_items)
	}

	$scope.refresh_seller_list = function()
	{
		 $http.get("http://34.232.210.211:3001/get-ebay-sellers-item/?format=json")
		    .then(function(response) {
		        $scope.items = response.data;
		        for(var i in $scope.items)
		        {
		        	$scope.items[i]["is_checked"] = false;
		        }
		    });
	}
});