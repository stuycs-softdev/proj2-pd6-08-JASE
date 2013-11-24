

curSort = "last";
curOrder = 1;

function updateSort(a,b){
    $.get("/js?param="+a+"&sort="+b,function(d){
	$("#sortTable").before(d).remove();
    });
}

function sort(a,b){
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