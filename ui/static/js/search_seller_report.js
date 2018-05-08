var searchSellerReportApp = angular.module('searchSellerReportApp', []);
searchSellerReportApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

searchSellerReportApp.controller('searchSellerReportCtrl', function($scope,$http) {
    $scope.keyword = "";
    $scope.reports = [];
    $scope.message = ""
    $scope.ebay_seller_reports = function()
	{
		search_keyword={};

		search_keyword["keyword"]=$scope.keyword;
		console.log("search_keyword",search_keyword)

        	$scope.cfdump = "";

        	var request = $http({
                    method: "get",
                    url: "/search-seller-reports-data/",
	                }).then(function(response) {
	                	console.log("reponse",response)
	                	console.log("response data", response.data["seller_reports"]);
	                	$scope.reports = response.data["seller_reports"]
                    });
	}
	console.log("search seller report app working.");
	$scope.ebay_seller_reports();

	$scope.start_search = function()
	{
		$http.get("/start-seller-search/"+$scope.keyword)
		    .then(function(response) {
		        alert(response.data["message"]);
		        console.log("response",response)
		    });
		search_keyword={};
		search_keyword["keyword"]=$scope.keyword;

	}
	$scope.viewSearchResult = function(report_id)
	{
		$http.get("/search-seller/"+report_id)
		    .then(function(response) {
		        // alert("start_search"+response);
		        console.log("response",response)
				$scope.ebay_seller_reports();

		    });
		search_keyword={};
		search_keyword["keyword"]=$scope.keyword;
		console.log("search_keyword",search_keyword);

	}
// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = jQuery.trim(cookies[i]);
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
});
