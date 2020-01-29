// ---- map setup ----
var mymap = L.map('map', {minZoom: 3,
  maxBounds:L.latLngBounds(L.latLng(-85.11013, -169.84589),L.latLng(84.98584,189.56085))})
  .setView([46.798333, 8.231944], 8);


// Définir les différentes couches de base:
var osmLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
});

// Ajouter la couche de base par défaut à la carte.
osmLayer.addTo(mymap);

// ---- bassin emploi poly -----
// var reg_lyr = L.geoJSON(bass_empl, {
//   style: function(feat){
//     return {
//       color: 'black',
//       stroke:'black',
//       // weight: 1,
//       // opacity: 0.5,
//       fillColor: 'blue',
//       // fillOpacity: 0.2,
//     }
//   },
//   onEachFeature: function(feat, lyr){
//     lyr.bindTooltip(
//       feat.properties.ID1, {
//         permanent: false,
//         sticky: true,
//         className: 'cordonLbl'
//       }
//     )
//   }
// });
var currentURL = null;
function getURL(){ currentURL = window.location.href; };
getURL(); // going to test the url to see if a bit of code runs. We want code to run
// on the events url and the listposts url but its two different functions that are called.

var polyStyle = {
  weight: 1,
  opacity: 0.5,
  color: 'blue',
  fillOpacity: 0.5,
  fillColor: 'blue'
}

var prevLayerClicked = null;
function onEachFeature(feature, layer) {
  var polyID = feature.properties.ID1;
  layer.on({
    mouseover: function(){
      this.setStyle({
        fillColor: 'red'
      });
      layer.bindTooltip(
        polyID, {
          pemanent: false,
          sticky: true
        }
      )
    },
    mouseout: function(){
      this.setStyle({
        fillColor: 'blue'
      });
    },
    click: function (e) {
      if (prevLayerClicked !== null){
        prevLayerClicked.setStyle(polyStyle);
      }
      var layer = e.target;
      layer.setStyle({
        weight: 1,
        color: '#fff',
        dashArray: '',
        fillOpacity: 0.9,
        fillColor: 'red'
      });
      prevLayerClicked = layer;
      $('[name="region"]').val(polyID, {passive: true});
    }
  });

  // var popupContent = "<p>I started out as a GeoJSON " +
  //     feature.geometry.type + ", but now I'm a Leaflet vector!</p>" + feature.properties.ID1;
  //
  // if (feature.properties && feature.properties.popupContent) {
  //   popupContent += feature.properties.popupContent;
  // }
  //
  // layer.bindPopup(popupContent);
}

if ( currentURL === 'http://127.0.0.1:5000/project' ) { // || currentURL === 'http://127.0.0.1:5000/listposts'
  L.geoJSON(bass_empl, {
    style: polyStyle,
    onEachFeature: onEachFeature
  }).addTo(mymap);
}

// reg_lyr.addTo(mymap);

// ---- markers ---- //
var marqueurs = [];

function show_posts(){
  // first remove all existing markers on page
  for (var i=0; i < marqueurs.length; i++){
    mymap.removeLayer(marqueurs[i])
  }
  // empty out container
  marqueurs = [];

  var url = '/posts.json';
  // json
  $.getJSON(url, function(data){
    console.log(data);
    for (var i=0; i < data.length; i++){
      var post = data[i];
      var m = L.marker([post.x, post.y]).addTo(mymap);
      m.info = post;
      // display marker info
      m.on('click', function(e) {
        var html = '<table cellpadding="3" id="marker_info">';
        html += '     <tr>';
        html += '       <td><b>Name:</b></td>';
        html += '       <td>' + e.target.info.name + '</td>';
        html += '     </tr>';
        html += '     <tr>';
        html += '       <td><b>Looking for: </b></td>';
        html += '       <td>' + e.target.info.talent_type + '</td>';
        html += '     </tr>';
        html += '     <tr>';
        html += '       <td><b>Description:</b></td>';
        html += '       <td>' + e.target.info.description + '</td>';
        html += '     </tr>';
        html += '     <tr>';
        html += '       <td><b>Email:</b></td>';
        html += '       <td>' + e.target.info.email + '</td>';
        html += '     </tr>';
        html += '     <tr>';
        html += '       <td><b>Date:</b></td>';
        html += '       <td>' + e.target.info.date + '</td>';
        html += '     </tr>';
        html += '     <tr>';
        html += '       <td><button type="button" onclick="console.log(123);">Contact!</button></td>';
        html += '     </tr>';
        html += '   </table>';
        $('#marker_info').remove();
        $('.info-box').html(html);
        $('#marker_info').insertAfter('#redirect-home');
        mymap.flyTo([e.target.info.x,e.target.info.y], 16);
        console.log(e);
      });
      marqueurs.push(m);
    }
  })
}

show_posts();

// ---- forms ----
function update_new_event(){
  var post = $.post("/form", function(data, status){
      alert("Data: " + data + "\nStatus: " + status);
    });
}

function post_concert() {
  var post = $.post("/concert-db", function(data, status){
    alert("Data: " + data + "\nStatus: " + status);
  })
}

function post_rec() {
  var post = $.post("/rec-db", function(data, status){
    alert("Data: " + data + "\nStatus: " + status);
  })
}

function post_event() {
  var post = $.post("/event-db", function(data, status){
    alert("Data: " + data + "\nStatus: " + status);
  })
}

function post_project() {
  var post = $.post("/project-db", function(data, status){
    alert("Data: " + data + "\nStatus: " + status);
  })
}

// ---- events ----
// Print coordinates of mouse on map using mousemove from leaflet
// mymap.on('mousemove',function(e){
//   var coord = e.latlng;
//   $('#mouse-coordonnees').html(coord.lat.toFixed(5) +' / '+ coord.lng.toFixed(5));
// });

// Set coordinates for form on mouse click from leaflet
mymap.on('click', function(e){
  var coord = e.latlng;
  // $('#coordonnees').html('Coordinates: ' + coord.lat.toFixed(5) +' / '+ coord.lng.toFixed(5));
  $('#lat').val(coord.lat.toFixed(4));
  $('#lng').val(coord.lng.toFixed(4));
})

// Set date to today
var date = new Date().toISOString().split('T')[0]
$('#date').val(date);

// region on click
// $('.leaflet-interactive').on('click', function(e) {
//   console.log(e);
// })

// Trigger flyto when most_recent_post button clicked
function most_recent_post() {
  $.getJSON('/posts.json', function(data){
    var mostResentEvent = data[0]; // !!! We are using this because evenements.json is ordered by id DESC!!!
    mymap.flyTo([mostResentEvent.x, mostResentEvent.y], 16)
    var html = '<table cellpadding="3" id="marker_info">';
    html += '     <tr>';
    html += '       <td><b>Name:</b></td>';
    html += '       <td>' + mostResentEvent.name + '</td>';
    html += '      </tr>';
    html += '     <tr>';
    html += '       <td><b>Looking for: </b></td>';
    html += '       <td>' + mostResentEvent.talent_type + '</td>';
    html += '      </tr>';
    html += '     <tr>';
    html += '       <td><b>Description:</b></td>';
    html += '       <td>' + mostResentEvent.description + '</td>';
    html += '      </tr>';
    html += '      <tr>';
    html += '        <td><b>Date:</b></td>';
    html += '        <td>' + mostResentEvent.date + '</td>';
    html += '      </tr>';
    html += '    </table>';
    $('#marker_info').remove();
    $('.info-box').html(html);
    $('#marker_info').insertAfter('#redirect-home');
  })
}

// ---- form change with user interaction ----
$("#tal_sel").change(function(){
  var tal = this.options[this.selectedIndex].value;
  if (tal == 'Musician'){
    $('#child_type').remove();
    var html = '<select id="child_type" name="child_type" form="form_holder">';
    html += '<option selected hidden>which one?</>';
    html += '<option name="person" value="Band">Band</>';
    html += '<option name="person" value="Pianist">Pianist</>';
    html += '<option name="person" value="Violinist">Violinist</>';
    html += '<option name="person" value="Bassist">Bassist</>';
    html += '<option name="person" value="Saxophonist">Saxophonist</>';
    html += '<option name="person" value="Guitarist">Guitarist</>';
    html += '<option name="person" value="Drummer">Drummer</>';
    html += '<option name="person" value="Singer">Singer</></select>';
    $('#form_holder').append(html);
    $('#child_type').insertAfter('#tal_sel');
    $('[name="description"]')
      .attr("placeholder", "Tell us about the music style, stage time, equipment, specific skills required...");
  } else if (tal == 'Photo/film'){
    $('#child_type').remove();
    var html = '<select id="child_type" name="child_type">';
    html += '<option selected hidden>which one?</>';
    html += '<option name="cam_person" value="Photographer">Photographer</>';
    html += '<option name="cam_person" value="Filmer">Filmer</>';
    html += '<option name="cam_person" value="Both">Both</>';
    $('#form_holder').append(html);
    $('#child_type').insertAfter('#tal_sel');
    $('[name="description"]')
      .attr("placeholder", "Tell us a little about what you need to capture");
  } else if (tal == 'Sound Engineer' || tal == 'VJ') {
    $('#child_type').remove();
    $('[name="description"]')
      .attr("placeholder", "What is the available equipment? Talk about the venue");
  } else {
    $('#child_type').remove();
  }

})
