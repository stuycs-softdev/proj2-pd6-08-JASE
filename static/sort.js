

curSort = "last";
curOrder = 1;
limit = 20;
offset = 0;

function updateSort(a,b){
    $.get("/js?param="+a+"&sort="+b+"&offset=0",function(d){
	$("#sortTable").before(d).remove();
    });
}

function sort(a,b){
    offset = 0;
    if(curSort == a) curOrder *= -1;
    else {
	curSort = a;
	curOrder = b;
    }
    updateSort(curSort,curOrder);
}			   
    


function viewmore(a){
    $(a).parent().parent().next().toggle();
}


function loadMore(){
    offset += limit;
    $.get("/js?param="+curSort+"&sort="+curOrder+"&offset="+offset,function(d){
	$("#loadMore").before(d);
    });
}