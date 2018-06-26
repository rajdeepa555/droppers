var pendingItemsApp = angular.module('pendingItemsApp', []);
pendingItemsApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});
pendingItemsApp.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);

    for (var i=0; i<total; i++) {
      input.push(i);
    }

    return input;
  };
});
pendingItemsApp.controller('pendingItemsCtrl', function($scope,$http,$timeout) {
    $scope.firstName = "John";
    $scope.lastName = "Doe";
    $scope.items = [{'title': 'Kickers Kick Hi Mens Black Red Blue Leather Ankle Boots Size 6-11', 'price': '', 'item_sold': '48+ Sold','is_checked':true}];
	
	$scope.items = [];
    $scope.keyword = "";
    $scope.pagination = {"has_next":false,"has_previous":false,"current_page":-1,"total_pages":-1,"previous_page_number":-1,"next_page_number":-1};
    $scope.selected_sorting_option = "";
    $scope.is_select = false;
	$scope.start_search = function()
	{
		alert($scope.keyword);
		$http.get("/start-seller-search/"+$scope.keyword)
		    .then(function(response) {
		        alert(response);
		    });
		search_keyword={};
		search_keyword["keyword"]=$scope.keyword;
		console.log("search_keyword",search_keyword)

        	$scope.cfdump = "";

        	var request = $http({
                    method: "post",
                    url: "/get-sellers-item/",
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
	$scope.delete = function()
	{
		var submit_items=[]
		for(var i in $scope.items)
		{
			if($scope.items[i]["is_checked"]==true)
			{
				submit_items.push($scope.items[i]["pk"])

			}
		}

	var csrftoken = getCookie('csrftoken');
    var headers = {};
    headers["X-CSRFToken"] = csrftoken;

		console.log("pk",submit_items)
		var request = $http({
                method: "post",
                url: "/delete-pending-ebay-items/",
                data: submit_items,
                headers:headers,
            }).then(function(response,headers) {
				$scope.refresh_seller_list(1);
	});
	}

	$scope.refresh_seller_list = function(page_number)
	{
		 console.log("page_number",page_number)
		$http.get("/get-pending-items/?format=json&page="+page_number+"&keyword="+$scope.keyword+"&order_by="+$scope.selected_sorting_option)
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
		    		console.log("!!!",$scope.items[i]["pk"])

		        }
		    });
		     console.log("blaaa",page_number)

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
