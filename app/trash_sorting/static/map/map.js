var map;
var view;
var user_point = null;

require([
  "esri/Graphic",
  "esri/Map",
  "esri/views/MapView",
  "esri/symbols/SimpleMarkerSymbol"
], function(Graphic, Map, MapView, SimpleMarkerSymbol) {

    map = new Map({
        basemap: "topo-vector"
    });

    view = new MapView({
        container: "viewDiv",
        map: map,
        center: [-118.80500, 34.02700], // longitude, latitude
        zoom: 13
    });


    document.getElementById("viewDiv").addEventListener("click", on_map_click);
    document.getElementById("viewDiv").addEventListener("drag", on_map_drag);

    function on_map_click(evt){
        var rect = evt.target.getBoundingClientRect();
        user_point = view.toMap({ x: evt.clientX -rect.left, y: evt.clientY -rect.top })
        view.graphics.removeAll();
        view.graphics.add(new Graphic(
            user_point,
            new SimpleMarkerSymbol({
              style: "diamond",
              color: "red",
              size: "8px",  // pixels
              outline: {  // autocasts as esri/symbols/SimpleLineSymbol
                color: [ 255, 0, 0 ],
                width: 3  // points
              }
            })
        ));
    }
});


function validate_coords_choice(){
    console.log('"new_search": 1, "lat": '+user_point.latitude.toFixed(3) + ', "lon": '+user_point.longitude.toFixed(3))
    post_search_with_args('"new_search": 1, "lat": '+user_point.latitude.toFixed(3) + ', "lon": '+user_point.longitude.toFixed(3))
}

