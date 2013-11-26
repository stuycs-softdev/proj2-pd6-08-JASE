

curSort = "last";
curOrder = 1;
limit = 20;
offset = 0;



function loading(text){
    $("#loading").remove();
    $("#opac").css("opacity",".2");
    $("body").append('<div id="loading" style="position:fixed;left:30%;right:30%;width:40%;top:30%;"><table class="table" style="border:2px solid black;"><tr class="active"><td style="text-align:center;"><br /><div style="margin-left:30%;margin-right:30%;width:40%;" class="progress progress-striped active"><div class="progress-bar" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%;"><span class="sr-only">Loading...</span></div></div>'+text+'</td></tr></table></div>');
}

function stopLoading(){
    $("#loading").remove();
    $("#opac").css("opacity","1");
}


function updateSort(a,b){
    $.get("/js?type=1&param="+a+"&sort="+b+"&offset=0",function(d){
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


function mapZoomOut(){
    var a = $("#mapImg").attr("src")
    var zoom = a.split("zoom=")[1].split("&")[0]*1-1
    if(zoom > 0)
	$("#mapImg").attr("src",a.replace(/zoom=(\d+)/i,"zoom="+zoom))
}
function mapZoomIn(){
    var a = $("#mapImg").attr("src")
    var zoom = a.split("zoom=")[1].split("&")[0]*1+1
    if(zoom < 20)
	$("#mapImg").attr("src",a.replace(/zoom=(\d+)/i,"zoom="+zoom))
}


$(function(){
    if(location.href.match("/teacher-")){
	$("tr.mapListing").click(function(){
	    $(this).parent().children("tr.success").attr("class","warning");
	    $(this).attr("class","success");
	    a = $(this).children("td:eq(0)").children("a").text().replace(" ","+")
	    $("#mapImg").attr("src","http://maps.googleapis.com/maps/api/staticmap?center="+a+"&zoom=13&size=600x300&maptype=roadmap&markers=color:red%7Clabel:A%7C"+a+"&sensor=false")
	});
    }
});