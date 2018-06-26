var searchSellerApp = angular.module('searchSellerApp', []);
searchSellerApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});
searchSellerApp.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);

    for (var i=0; i<total; i++) {
      input.push(i);
    }

    return input;
  };
});
searchSellerApp.controller('searchSellerCtrl', function($scope,$http,$timeout,$location) {
    var url = $location.absUrl().split('/')

    $scope.firstName = "John";
    $scope.lastName = "Doe";
    $scope.report_id = url[url.length - 2]
    console.log("urlll",$scope.report_id)
    $scope.items = [{'title': 'Kickers Kick Hi Mens Black Red Blue Leather Ankle Boots Size 6-11', 'price': '', 'item_sold': '48+ Sold','is_checked':true}];
	
	$scope.items = [];
    $scope.keyword = "";
    $scope.pagination = {"has_next":false,"has_previous":false,"current_page":-1,"total_pages":-1,"previous_page_number":-1,"next_page_number":-1};
    $scope.selected_sorting_option = "";
    $scope.is_select = false
	// $scope.start_search = function()
	// {
	// 	alert($scope.keyword);
	// 	$http.get("/start-seller-search/"+$scope.keyword)
	// 	    .then(function(response) {
	// 	        alert("start_search"+response);
	// 	        console.log("response",response)
	// 	    });
	// 	search_keyword={};
	// 	search_keyword["keyword"]=$scope.keyword;
	// 	console.log("search_keyword",search_keyword);

	// }    

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
				submit_items.push($scope.items[i]["pk"])

			}
		}
		console.log("pk",submit_items)
		var csrftoken = getCookie('csrftoken');
        var headers = {};
        headers["X-CSRFToken"] = csrftoken;
		var request = $http({
                method: "post",
                url: "/pending-ebay-items/",
                // transformRequest: transformRequestAsFormPost,
                data: submit_items,
                headers:headers
                // headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            });
	    alert("Items added to pending list");
	    $scope.refresh_seller_list(1);

	}

	$scope.refresh_seller_list = function(page_number)
	{
		console.log("report report_id",$scope.report_id)
		$http.get("/get-sellers-item/?format=json&page="+page_number+"&report_id="+$scope.report_id+"&order_by="+$scope.selected_sorting_option)
		    .then(function(response) {
		        $scope.items = response.data["items_list"];
		        $scope.pagination["has_next"] = response.data["has_next"];
		        $scope.pagination["has_previous"] = response.data["has_previous"];
		        $scope.pagination["current_page"] = response.data["current_page_number"];
		        $scope.pagination["next_page_number"] = response.data["next_page_number"];
		        $scope.pagination["previous_page_number"] = response.data["previous_page_number"];
		        $scope.pagination["total_pages"] = response.data["total_page"];
		        console.log("total_pages",$scope.pagination["total_pages"])
		        for(var i in $scope.items)
		        {
		        	$scope.items[i]["is_checked"] = false;

		        }
		    });
	}
	$scope.refresh_seller_list(1);
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