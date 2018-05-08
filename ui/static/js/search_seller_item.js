var searchSellerItemApp = angular.module('searchSellerItemApp', ['uiSwitch']);
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
    $scope.ignored_items = [];
    $scope.unmonitored_items = [];
    $scope.keyword = "";
    $scope.pagination = {"has_next":false,"has_previous":false,"current_page":-1,"total_pages":-1,"previous_page_number":-1,"next_page_number":-1};
    $scope.unmonitored_pagination = {"has_next":false,"has_previous":false,"current_page":-1,"total_pages":-1,"previous_page_number":-1,"next_page_number":-1};
    $scope.ignored_pagination = {"has_next":false,"has_previous":false,"current_page":-1,"total_pages":-1,"previous_page_number":-1,"next_page_number":-1};
    $scope.selected_sorting_option = "";
    $scope.selected_pagination_option = "50";
    $scope.is_select = false;
    $scope.count_ignored = ""
    $scope.count_monitored = ""
    $scope.count_unmonitored = ""
    $scope.start_search = function()
	{
		search_keyword={};
		search_keyword["keyword"]=$scope.keyword;
		console.log("search_keyword",search_keyword)

        	$scope.cfdump = "";

        	var request = $http({
                    method: "post",
                    url: "/get-ebay-sellers-item/",
                    // transformRequest: transformRequestAsFormPost,
                    data: search_keyword
	                });

        	request.success(
                    function( html ) {
                        $scope.cfdump = html;
                    }
                );
	}  
	
	$scope.formonitored = function(){
		 $scope.current_tab = 'monitored'
		console.log($scope.current_tab);
	}

	$scope.forunmonitored = function(){
		 $scope.current_tab = 'unmonitored'
		console.log($scope.current_tab);
	}

	$scope.forignored = function(){
		 $scope.current_tab = 'ignored'
		console.log($scope.current_tab);
	}

	$scope.select_all = function(){
			// console.log("select_all",$scope.is_select)
			if($scope.current_tab == 'monitored')	
				{$scope.select_monitored();console.log("select all checkbox from monitored tab")}
			else if($scope.current_tab == 'unmonitored') 
				{ $scope.select_umonitored();console.log("select all checkbox from unmonitored tab")}
			else{$scope.select_ignored();console.log("select all checkbox from ignored tab")}
		};

	$scope.select_monitored = function(){
		$timeout(function(){
			// console.log("select_all",$scope.is_select)
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

	}

	$scope.select_umonitored = function(){
		$timeout(function(){
			// console.log("select_all",$scope.is_select)
			if($scope.is_select==false){
				for(var i in $scope.unmonitored_items)
		        {
		        	$scope.unmonitored_items[i]["is_checked"] = true;
		        }
		        $scope.is_select = true
		    }
		    else{
				for(var i in $scope.unmonitored_items)
		    	{
		        	$scope.unmonitored_items[i]["is_checked"] = false;
		        }
		        $scope.is_select = false
		    }
		}, 500);

	}

	$scope.select_ignored = function(){
		$timeout(function(){
			// console.log("select_all",$scope.is_select)
			if($scope.is_select==false){
				for(var i in $scope.ignored_items)
		        {
		        	$scope.ignored_items[i]["is_checked"] = true;
		        }
		        $scope.is_select = true
		    }
		    else{
				for(var i in $scope.ignored_items)
		    	{
		        	$scope.ignored_items[i]["is_checked"] = false;
		        }
		        $scope.is_select = false
		    }
		}, 500);

	}

	$timeout(function(){
		$scope.update_ebay_info = function(index,ebay_id,amazon_sku)
		{
			var csrf_token = document.getElementById("csrf_token").value;
			var form_data = {"csrfmiddlewaretoken":csrf_token,"values":[{"ebay_id":ebay_id,"amazon_sku":amazon_sku}]};
			 var request = $http({
	                    method: "post",
	                    url: "/update-ebay-items/",
	                    data: form_data,
	                }).then(function(data){
						 alert("Updated Successfully");
						 $window.location.reload();
			 			 $scope.refresh_seller_list(1);
	                });
		}
	},1000);
	$scope.check_value = function(value)
	{	
		alert(value);
	}
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
						var submit_data={};
						ebay_id=$scope.items[i]["ebay_id"];
						amazon_sku=$scope.items[i]["custom_label"];
						submit_data = {"ebay_id":ebay_id,"amazon_sku":amazon_sku};
						list_of_ids.push(submit_data);
					}
			}
			for(var i in $scope.unmonitored_items)
			{
				
				if($scope.unmonitored_items[i]["is_checked"]==true)
					{
						var csrf_token = document.getElementById("csrf_token").value;
						var submit_data={};
						ebay_id=$scope.unmonitored_items[i]["ebay_id"];
						amazon_sku=$scope.unmonitored_items[i]["custom_label"];
						submit_data = {"ebay_id":ebay_id,"amazon_sku":amazon_sku};
						list_of_ids.push(submit_data);
					}
			}
			for(var i in $scope.ignored_items)
			{
				
				if($scope.ignored_items[i]["is_checked"]==true)
					{
						var csrf_token = document.getElementById("csrf_token").value;
						var submit_data={};
						ebay_id=$scope.ignored_items[i]["ebay_id"];
						amazon_sku=$scope.ignored_items[i]["custom_label"];
						submit_data = {"ebay_id":ebay_id,"amazon_sku":amazon_sku};
						list_of_ids.push(submit_data);
					}
			}
			form_data["values"] = list_of_ids;
			var request = $http({
	                    method: "post",
	                    url: "/update-ebay-items/",
	                    data: form_data,
	                });
			alert("Updated Successfully");
			$window.location.reload();
			$scope.refresh_seller_list(1);
		}
	},1000);
	$scope.is_flag = function()
	{
		var csrf_token = document.getElementById("csrf_token").value;

		var values=[]
		for(var i in $scope.items)
		{
			console.log("monitored falg",$scope.items[i]["flag"])

			if($scope.items[i]["flag"] == true)
			{
			submit_items = {}
			console.log("is_select monnitored",$scope.items[i]["flag"])
			submit_items["ebay_id"] = $scope.items[i]["ebay_id"]
			submit_items["status"] = $scope.items[i]["status"]
			values.push(submit_items)
			}
		}
		for(var i in $scope.unmonitored_items)
		{
			if($scope.unmonitored_items[i]["flag"] == true)
			{
			submit_items = {}
			console.log("is_select nmonitored",$scope.unmonitored_items[i]["flag"])
			submit_items["ebay_id"] = $scope.unmonitored_items[i]["ebay_id"]
			submit_items["flag"] = $scope.unmonitored_items[i]["flag"]
			submit_items["status"] = $scope.unmonitored_items[i]["status"]
			values.push(submit_items)
			console.log("unmonitored falg",$scope.unmonitored_items[i]["flag"])
		}
		}
		for(var i in $scope.ignored_items)
		{
			if($scope.ignored_items[i]["flag"] == true)
			{
			submit_items = {}
			console.log("is_select ignored",$scope.ignored_items[i]["flag"])
			submit_items["ebay_id"] = $scope.ignored_items[i]["ebay_id"]
			submit_items["flag"] = $scope.ignored_items[i]["flag"]
			submit_items["status"] = $scope.ignored_items[i]["status"]
			values.push(submit_items)
			console.log("ignored falg",$scope.ignored_items[i]["flag"])
			}
		}
		var form_data = {"csrfmiddlewaretoken":csrf_token,"values":values};

		var request = $http({
            method: "post",
            url: "/flag-seller-ebay-items/",
            data: form_data,
        }).then(function(response) {
			$scope.refresh_seller_list(1);
			$scope.refresh_unmonitored_list(1);
			$scope.refresh_ignored_list(1);
	});

	}
	$scope.edit_bulk = function()
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
		for(var i in $scope.unmonitored_items)
		{
			if($scope.unmonitored_items[i]["is_checked"]==true)
			{
				submit_items.push($scope.unmonitored_items[i])
				console.log($scope.unmonitored_items[i]["is_checked"])

			}
		}
		for(var i in $scope.ignored_items)
		{
			if($scope.ignored_items[i]["is_checked"]==true)
			{
				submit_items.push($scope.ignored_items[i])
				console.log($scope.ignored_items[i]["is_checked"])

			}
		}
		var request = $http({
	                    method: "get",
	                    url: "/edit-ebay-items/",
	                    // transformRequest: transformRequestAsFormPost,
	                    data: submit_items,
	                    // headers: {'Content-Type': 'application/x-www-form-urlencoded'}
	                });
	}

	$scope.edit_ebay_item = function(ebay_id)
	{
		console.log("ebay_id",ebay_id)
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
	                    url: "/add-ebay-sellers-item/",
	                });	
		
	}

	$scope.update_all = function()
	{
		var request = $http({
	                    method: "post",
	                    url: "/update-all-ebay-items/",
	                });	
		
	}



	$scope.refresh_ignored_list = function(page_number)
	{
		console.log("ignord pfage",$scope.selected_pagination_option)
		$http.get("/get-ebay-sellers-itemm/?format=json&page="+page_number+"&keyword="+$scope.keyword+"&page_by="+$scope.selected_pagination_option+"&order_by="+$scope.selected_sorting_option+"&status=ignored")
		    .then(function(response) {
		    	$scope.ignored_items = [];
		    	$scope.count_ignored = 0;
		    	if("ignored" in response.data){
		    		$scope.ignored_items = response.data["ignored"]["items_list"];
		        $scope.ignored_pagination["has_next"] = response.data["has_next"];
		        $scope.ignored_pagination["has_previous"] = response.data["has_previous"];
		        $scope.ignored_pagination["current_page"] = response.data["current_page_number"];
		        $scope.ignored_pagination["next_page_number"] = response.data["next_page_number"];
		        $scope.ignored_pagination["previous_page_number"] = response.data["previous_page_number"];
		        $scope.ignored_pagination["total_pages"] = response.data["total_page"];
		        for(var i=0;i<response.data["count_status"].length;i++)
		        {	
		        	console.log("status error",response.data["count_status"])
		        	if(response.data["count_status"][i]["status"] == 'monitored')
		        	{
		        		$scope.count_monitored = response.data["count_status"][i]["total"]
		        	}
		        	if(response.data["count_status"][i]["status"] == 'unmonitored')
		        	{
		        		$scope.count_unmonitored = response.data["count_status"][i]["total"]
		        	}
		        	if(response.data["count_status"][i]["status"] == 'ignored')
		        	{
		        		$scope.count_ignored = response.data["count_status"][i]["total"]
		        	}
		        }
		        // $scope.count_status = response.data["count_status"]
		        for(var i in $scope.ignored_items)
		        {
		        	$scope.ignored_items[i]["is_checked"] = false;
		        	$scope.ignored_items[i]["flag"] = false;
		        }
			// $scope.refresh_seller_list(1);

		    }
		    });
	}
		$scope.refresh_unmonitored_list = function(page_number)
	{
		console.log("unmonitored pfage",$scope.selected_pagination_option)

		$http.get("/get-ebay-sellers-itemm/?format=json&page="+page_number+"&keyword="+$scope.keyword+"&order_by="+$scope.selected_sorting_option+"&page_by="+$scope.selected_pagination_option+"&status=unmonitored")
		    .then(function(response) {
		    	$scope.unmonitored_items = [];
		    	$scope.count_unmonitored = 0;
		    	if("unmonitored" in response.data){
		        $scope.unmonitored_items = response.data["unmonitored"]["items_list"];
		        $scope.unmonitored_pagination["has_next"] = response.data["has_next"];
		        $scope.unmonitored_pagination["has_previous"] = response.data["has_previous"];
		        $scope.unmonitored_pagination["current_page"] = response.data["current_page_number"];
		        $scope.unmonitored_pagination["next_page_number"] = response.data["next_page_number"];
		        $scope.unmonitored_pagination["previous_page_number"] = response.data["previous_page_number"];
		        $scope.unmonitored_pagination["total_pages"] = response.data["total_page"];
		        // $scope.count_status = response.data["count_status"]
		        for(var i=0;i<response.data["count_status"].length;i++)
		        {	
		        	console.log("status error",response.data["count_status"])
		        	if(response.data["count_status"][i]["status"] == 'monitored')
		        	{
		        		$scope.count_monitored = response.data["count_status"][i]["total"]
		        	}
		        	if(response.data["count_status"][i]["status"] == 'unmonitored')
		        	{
		        		$scope.count_unmonitored = response.data["count_status"][i]["total"]
		        	}
		        	if(response.data["count_status"][i]["status"] == 'ignored')
		        	{
		        		$scope.count_ignored = response.data["count_status"][i]["total"]
		        	}
		        }

		        for(var i in $scope.unmonitored_items)
		        {
		        	$scope.unmonitored_items[i]["is_checked"] = false;
		        	$scope.unmonitored_items[i]["flag"] = false;
		        }
			// $scope.refresh_ignored_list(1);

		    }
		    });
	}

	
	$scope.refresh_unmonitored_list(1);
	$scope.refresh_ignored_list(1);
	$scope.refresh_seller_list = function(page_number)
	{
		 $http.get("/get-ebay-sellers-itemm/?format=json&page="+page_number+"&keyword="+$scope.keyword+"&order_by="+$scope.selected_sorting_option+"&page_by="+$scope.selected_pagination_option+"&status=monitored")
		    .then(function(response) {
		    	$scope.items = [];
		    	$scope.count_monitored = 0;
		    	if("monitored" in response.data){
		    		$scope.items = response.data["monitored"]["items_list"];
			        $scope.pagination["has_next"] = response.data["has_next"];
			        $scope.pagination["has_previous"] = response.data["has_previous"];
			        $scope.pagination["current_page"] = response.data["current_page_number"];
			        $scope.pagination["next_page_number"] = response.data["next_page_number"];
			        $scope.pagination["previous_page_number"] = response.data["previous_page_number"];
			        $scope.pagination["total_pages"] = response.data["total_page"];
			        $scope.count_monitored = response.data["count_status"]["monitored"]
			        $scope.count_unmonitored = response.data["count_status"]["unmonitored"]
			        $scope.count_ignored = response.data["count_status"]["ignored"]
			        for(var i=0;i<response.data["count_status"].length;i++)
			        {	
			        	console.log("status error",response.data["count_status"])
			        	if(response.data["count_status"][i]["status"] == 'monitored')
			        	{
			        		$scope.count_monitored = response.data["count_status"][i]["total"]
			        	}
			        	if(response.data["count_status"][i]["status"] == 'unmonitored')
			        	{
			        		$scope.count_unmonitored = response.data["count_status"][i]["total"]
			        	}
			        	if(response.data["count_status"][i]["status"] == 'ignored')
			        	{
			        		$scope.count_ignored = response.data["count_status"][i]["total"]
			        	}
			        }
			        console.log("stttt",$scope.count_ignored,response.data["count_status"][0]["total"],response.data["count_status"])
			        for(var i in $scope.items)
			        {
			        	$scope.items[i]["is_checked"] = false;
			        	$scope.items[i]["flag"] = false;
			        	// console.log("flag",$scope.items[i]["flag"])
			        }
		    	}
		    });
		 

	}
	$scope.refresh_seller_list(1);

	$scope.search = function()
	{
		$scope.refresh_seller_list(1);
		$scope.refresh_unmonitored_list(1);
		$scope.refresh_ignored_list(1);
	}

	$scope.all_lists = function(page_number)
	{
		console.log("1");
		$scope.refresh_unmonitored_list(page_number);
		console.log("2");

		$scope.refresh_ignored_list(page_number);
		console.log("3");
		$scope.refresh_seller_list(page_number);
	}	
	$scope.open_marginModel = function(ebay_id)
	{	console.log("ebay_id",ebay_id)
		$("#marginModal #ebay-id").val(ebay_id);
		$("#marginModal").modal("toggle")
	}
	$scope.open_stockModel = function(ebay_id)
	{	console.log("ebay_id",ebay_id)
		$("#stockModal #ebay_id_stock").val(ebay_id);
		$("#stockModal").modal("toggle")
	}
});

