var searchSellerItemApp = angular.module('searchSellerItemApp', []);
searchSellerItemApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});
searchSellerItemApp.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);

    for (var i=0; i<total; i++) {
      input.push(i);
    }

    return input;
  };
});

searchSellerItemApp.controller('searchSellerItemCtrl', function($scope,$http,$timeout,$window) {
    $scope.items = [];
    $scope.keyword = "";
    $scope.products = [{"id":"1","name":"p1","is_checked":false},{"id":"2","name":"p2","is_checked":false},{"id":"3","name":"p3","is_checked":false}];
    $scope.pagination = {"has_next":false,"has_previous":false,"current_page":-1,"total_pages":-1,"previous_page_number":-1,"next_page_number":-1};
    $scope.selected_sorting_option = "";
    $scope.is_select = false;
    $scope.start_search = function()
	{
		search_keyword={};
		search_keyword["keyword"]=$scope.keyword;
		console.log("search_keyword",search_keyword)

        	$scope.cfdump = "";

        	var request = $http({
                    method: "post",
                    url: "http://34.232.210.211:3001/get-ebay-sellers-item/",
                    // transformRequest: transformRequestAsFormPost,
                    data: search_keyword
                });

        	request.success(
                    function( html ) {
                        $scope.cfdump = html;
                    }
                );
	}    
	$scope.select_all = function(){
		$timeout(function(){
			console.log("select_all",$scope.is_select)
			if($scope.is_select==false){
				for(var i in $scope.items)
		        {
		        	$scope.items[i]["is_checked"] = true;
		        }
		        $scope.is_select = true
		    }
		    else{
				for(var i in $scope.items)
		    	{
		        	$scope.items[i]["is_checked"] = false;
		        }
		        $scope.is_select = false
		    }
		}, 500);

		// $scope.$apply();
	}
	$timeout(function(){
		$scope.update_ebay_info = function(index,ebay_id,amazon_sku)
		{
			var csrf_token = document.getElementById("csrf_token").value;
			// alert("csrf_token"+csrf_token);
			// alert(index);
			// alert(ebay_id);
			// var ebay_id = "263288532885";
			// var amazon_sku = "B0028OJAIY";
			var form_data = {"csrfmiddlewaretoken":csrf_token,"values":[{"ebay_id":ebay_id,"amazon_sku":amazon_sku}]};
			 var request = $http({
	                    method: "post",
	                    url: "http://34.232.210.211:3001/update-ebay-items/",
	                    data: form_data,
	                }).then(function(data){
						 alert("Updated Successfully");
						 $window.location.reload();
			 			 $scope.refresh_seller_list(1);
	                });
		}
	},1000);
	$timeout(function(){
		$scope.update_bulk_ebay_info = function()
		{
			var form_data={};
			var list_of_ids = [];
			for(var i in $scope.items)
			{
				
				if($scope.items[i]["is_checked"]==true)
					{
						var csrf_token = document.getElementById("csrf_token").value;
						// alert("csrf_token"+csrf_token);
						// alert(index);
						// alert(ebay_id);
						// var ebay_id = "263288532885";
						// var amazon_sku = "B0028OJAIY";
						var submit_data={};
						ebay_id=$scope.items[i]["ebay_id"];
						amazon_sku=$scope.items[i]["custom_label"];
						console.log("amazon_sku",amazon_sku);
						console.log("ebay_id",ebay_id);
						submit_data = {"ebay_id":ebay_id,"amazon_sku":amazon_sku};
						list_of_ids.push(submit_data);
					}
			}
			form_data["values"] = list_of_ids;
			var request = $http({
	                    method: "post",
	                    url: "http://34.232.210.211:3001/update-ebay-items/",
	                    // transformRequest: transformRequestAsFormPost,
	                    data: form_data,
	                    // headers: {'Content-Type': 'application/x-www-form-urlencoded'}
	                });
			alert("Updated Successfully");
			$window.location.reload();
			$scope.refresh_seller_list(1);
		}
	},1000);
	$scope.submit = function()
	{
		var submit_items=[];
		for(var i in $scope.items)
		{
			if($scope.items[i]["is_checked"]==true)
			{
				submit_items.push($scope.items[i]);
				console.log($scope.items[i]["is_checked"]);

			}
		}
		console.log(submit_items);

	}
	$scope.edit_bulk = function()
	{
		var submit_items=[];
		for(var i in $scope.items)
		{
			if($scope.items[i]["is_checked"]==true)
			{
				submit_items.push($scope.items[i]);
				console.log($scope.items[i]["is_checked"]);

			}
		}
		var request = $http({
	                    method: "get",
	                    url: "http://34.232.210.211:3001/edit-ebay-items/",
	                    // transformRequest: transformRequestAsFormPost,
	                    data: submit_items,
	                    // headers: {'Content-Type': 'application/x-www-form-urlencoded'}
	                });
	}

	$scope.edit_ebay_item = function(ebay_id)
	{
		console.log("ebay_id",ebay_id);
		// var submit_items=[]
		// for(var i in $scope.items)
		// {
		// 	if($scope.items[i]["is_checked"]==true)
		// 	{
		// 		submit_items.push($scope.items[i])
		// 		console.log($scope.items[i]["is_checked"])

		// 	}
		// }
		// console.log(submit_items)
	}

	$scope.refresh_db = function()
	{
		var request = $http({
	                    method: "get",
	                    url: "http://34.232.210.211:3001/add-ebay-sellers-item/",
	                });	
		
	}

	$scope.refresh_seller_list = function(page_number)
	{
		 $http.get("http://34.232.210.211:3001/get-ebay-sellers-item/?format=json&page="+page_number+"&keyword="+$scope.keyword+"&order_by="+$scope.selected_sorting_option)
		    .then(function(response) {
		        $scope.items = response.data["items_list"];
		        $scope.pagination["has_next"] = response.data["has_next"];
		        $scope.pagination["has_previous"] = response.data["has_previous"];
		        $scope.pagination["current_page"] = response.data["current_page_number"];
		        $scope.pagination["next_page_number"] = response.data["next_page_number"];
		        $scope.pagination["previous_page_number"] = response.data["previous_page_number"];
		        $scope.pagination["total_pages"] = response.data["total_page"];
		        for(var i in $scope.items)
		        {
		        	$scope.items[i]["is_checked"] = false;
		        }
		    });
		    // $scope.$apply();
	}
	$scope.refresh_seller_list(1);
});