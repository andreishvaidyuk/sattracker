window.onload = function () {
        mapboxgl.accessToken = 'pk.eyJ1IjoiYW5kcmV5c2h2YWlkeXVrIiwiYSI6ImNqdm9uNnRjNTBqNWs0YXJoMDB6eTBnbG4ifQ.U7TPQYPkg78E4Fdvv1k42Q';
        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [0,20],
            zoom: 1.1,
        });

        var url = 'map.geojson';
        map.on('load', function () {
            window.setInterval(function() {
                map.getSource('satellite').setData(url);
            }, 5000);

            map.addLayer({
                "id": "satellite",
                "type": "symbol",
                "source": {
                    type: 'geojson',
                    data: url,
                },
                "layout": {
                    "icon-image": "rocket-15"
                }
            });

            map.addLayer({
                "id": "antenna",
                "type": "symbol",
                "source": {
                    "type": "geojson",
                    "data": {
                        "type": "FeatureCollection",
                        "features": [{
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [71.383393, 51.076597]
                            }
                        }]
                    }
                    },
                "layout": {
                    "icon-image": "place-of-worship-15"
                }
            });
        });
};