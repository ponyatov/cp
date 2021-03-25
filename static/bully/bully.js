
sio.on('localtime',(msg)=>{
    console.log('sio','localtime','bully',msg)
    $('#timestamp').html( msg.date +"<br>"+ msg.time )
    $('#date').val(msg.isodate)
})

sio.on('area',(msg)=>{
    console.log('sio','area','bully',msg)
    area
        .clearLayers()
        .addLayer(L.geoJSON( msg.geojson ), {className: 'map-area'})
    map
        .fitBounds( msg.bounds )
})

sio.on('location',(msg)=>{
    console.log('sio','location',msg)
    L.circleMarker([ msg.lat,msg.lng ],{radius:3,opacity:1})
        .bindTooltip(`${msg.name}<br>${msg.forecast}`, {
            permanent:true, interactive: true, direction: msg.align })
        // .bindPopup(`${msg.name}`,{className: 'map-popup'})
        // .addEventListener('click', function(e){console.log(e)})
    .addTo(area)
})

function gui_onchange(gid,name,value) {
    console.log('gui/onchange',[gid,name,value])
    sio.emit('gui/onchange',[gid,name,value])
}
