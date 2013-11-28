
function initialize() {
  var myLatlng = new google.maps.LatLng(40.7143528,-73.90597309999999);
  var mapOptions = {
    zoom: 13,
    center: myLatlng
  }
  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

/*  for(x=0;x<addr.length;x++){
    var marker = new google.maps.Marker({
      position: new google.maps.LatLng(addr[x][1],addr[x][2]),
      map: map,
      title: addr[x][0]
    });
    google.maps.event.addListener(marker,"click",function(){
      alert("clicked");
    });
  }*/
}

google.maps.event.addDomListener(window, 'load', initialize);
