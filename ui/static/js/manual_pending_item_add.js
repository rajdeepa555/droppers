var manualPendingItemAddApp = angular.module('manualPendingItemAddApp', []);
manualPendingItemAddApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});
manualPendingItemAddApp.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);

    for (var i=0; i<total; i++) {
      input.push(i);
    }

    return input;
  };
});
manualPendingItemAddApp.controller('manualPendingItemAddCtrl', function($scope,$http,$timeout,$window) {
    $scope.firstName = "John";
    $scope.lastName = "Doe";
	$scope.items = [];
	$scope.urls = "";
    $scope.keyword = "";
    $scope.pagination = {"has_next":false,"has_previous":false,"current_page":-1,"total_pages":-1,"previous_page_number":-1,"next_page_number":-1};
    $scope.selected_sorting_option = "";
    $scope.is_select = false
	$scope.start_search = function()
	{
		var csrftoken = getCookie('csrftoken');
        var headers = {};
        headers["X-CSRFToken"] = csrftoken;
		alert("Please wait while items are being searched.")
		var search_keyword = {"keyword":$scope.urls}
		$http({
                    method: "post",
                    url: "/search-amazon-item/",
                    data: search_keyword,
					headers: headers
                }).then(function(response) {
		        $scope.items = response.data["details"];

		    });

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
	$scope.added_to_pending= function()
	{
		var submit_items=[]
		for(var i in $scope.items)
		{
			if($scope.items[i]["is_checked"]==true)
			{
				submit_items.push($scope.items[i])

			}
		}
		console.log("pk",submit_items)
		var csrftoken = getCookie('csrftoken');
        var headers = {};
        headers["X-CSRFToken"] = csrftoken;
		var request = $http({
                method: "post",
                url: "/pending-ebay-items/",
                data: submit_items,
                headers:headers
            }).then(function(response) {
			    alert("Items added to pending list");


		    });
	 //    $scope.refresh_seller_list(1);

	}

	// $scope.refresh_seller_list = function(page_number)
	// {
	// 	 console.log("page_number",page_number)
	// 	$http.get("http://34.232.210.211:3001/get-sellers-item/?format=json&page="+page_number+"&keyword="+$scope.keyword+"&order_by="+$scope.selected_sorting_option)
	// 	    .then(function(response) {
	// 	        $scope.items = response.data["items_list"];
	// 	        $scope.pagination["has_next"] = response.data["has_next"];
	// 	        $scope.pagination["has_previous"] = response.data["has_previous"];
	// 	        $scope.pagination["current_page"] = response.data["current_page_number"];
	// 	        $scope.pagination["next_page_number"] = response.data["next_page_number"];
	// 	        $scope.pagination["previous_page_number"] = response.data["previous_page_number"];
	// 	        $scope.pagination["total_pages"] = response.data["total_page"];
	// 	        console.log("total_pages",$scope.pagination["total_pages"])
	// 	        for(var i in $scope.items)
	// 	        {
	// 	        	$scope.items[i]["is_checked"] = false;
	// 	    		console.log("!!!",$scope.items[i]["pk"])

	// 	        }
	// 	    });
	// 	     console.log("blaaa",page_number)
	// }
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
