// Search Autocomplete
function initialize() {
    const input = document.getElementById('searchTextField');
    const options = {
        types: ['(cities)'],
    }
    new google.maps.places.Autocomplete(input, options);
}
google.maps.event.addDomListener(window, 'load', initialize);