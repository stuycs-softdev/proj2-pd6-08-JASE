plines = [];

function initialize() {
    var myLatlng = new google.maps.LatLng(40.7143528,-73.90597309999999);
    var mapOptions = {
	zoom: 13,
	center: myLatlng
    }
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    for(x=0;x<addr.length;x++){
	var marker = new google.maps.Marker({
	    position: new google.maps.LatLng(addr[x][1],addr[x][2]),
	    map: map,
	    title: addr[x][0]
	});
	google.maps.event.addListener(marker,"click",function(){
	    showData(this.title);
	});
    }
}

google.maps.event.addDomListener(window, 'load', initialize);



function showData(n){
    $.get("teacherjs-"+n.replace(" ","+"),function(d){
//	curPath = google.maps.geometry.encoding.decodePath(d.split(" ")[0])
	$("#sidebar").html(d)//.replace(d.split(" ")[0],""))
    });
}

function viewTransit(){
    for(x=0;x<plines.length;x++){
	plines[x].setMap(null);
    }

    dir = [];

    for(x=0;x<cp.length;x++){

	var strokeColor = '#000000', strokeWeight = 2;
	if(cp[x].travel_mode == "TRANSIT"){
	    strokeColor = cp[x].transit_details.line.color
	    strokeWeight = 5;
	}

	p = new google.maps.Polyline({
	    path: google.maps.geometry.encoding.decodePath(cp[x].polyline.points),
	    geodesic: true,
	    strokeColor: strokeColor,
	    strokeOpacity: 1.0,
	    strokeWeight: strokeWeight
	});
	p.setMap(map);
	plines[x] = p;

	if(cp[x].travel_mode == "TRANSIT"){
	    if(cp[x].transit_details.line.vehicle.type == "SUBWAY"){
		dir[x] = '<div style="background:'+cp[x].transit_details.line.color+';color:white;padding:5px"><strong>'+cp[x].transit_details.line.short_name+'</strong>: '+cp[x].transit_details.line.name+'</div><table><tr><td rowspan="3"><img src="'+cp[x].transit_details.line.icon+'" /></td><td>From <strong>'+cp[x].transit_details.departure_stop.name+'</strong></td></tr><tr><td>To <strong>'+cp[x].transit_details.arrival_stop.name+'</strong></td></tr><tr><td>'+cp[x].duration.text+', '+cp[x].transit_details.num_stops+' stops</td></tr></table>';
	    } else {
		dir[x] = '<div style="background:'+cp[x].transit_details.line.color+';color:white;padding:5px"><strong>'+cp[x].transit_details.line.short_name+'</strong>: '+cp[x].transit_details.line.name+'</div>From <strong>'+cp[x].transit_details.departure_stop.name+'</strong><br />To <strong>'+cp[x].transit_details.arrival_stop.name+'</strong><br />'+cp[x].duration.text+', '+cp[x].transit_details.num_stops+' stops';
	    }
	} else if(cp[x].travel_mode == "WALKING" && (x == 0 || x == cp.length-1)){
	    dir[x] = '<div style="background:black;color:white;padding:5px;">Walk</div>'+cp[x].html_instructions+'<br />'+cp[x].duration.text+', '+cp[x].distance.text;
	}
    }

    $("#publicTransitDetails").html("<table><tr><td>"+dir.join("</td></tr><tr><td>")+"</td></tr></table>");

}