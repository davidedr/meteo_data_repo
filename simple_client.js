// Simple JS client

var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

data_json = {
    location_id: 1,
    wind_speed_knots: 10,
    wind_direction_deg: 11,
    barometric_pressure_hPa: 12.1,
    rain_today_mm: 13,
    rain_rate_mmph: 14.1,
    temperature_cels: 15.1,
    rel_humidity: 0.16,
    uv_index: 17.1,
    heat_index_cels: 18.1
}
const data = JSON.stringify(data_json)

const xhr = new XMLHttpRequest()

xhr.addEventListener('readystatechange', function() {
    if (this.readyState === this.DONE) {
        console.log(this.responseText)
    }
})

xhr.open('POST', 'http://localhost:8080/api/meteo_data', false)
xhr.setRequestHeader('Content-Type', "application/json; charset=utf-8") // Content-Type is CASE SENSITVE!
xhr.send(data)