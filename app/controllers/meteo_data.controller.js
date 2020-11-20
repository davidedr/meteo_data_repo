const db = require("../models")
const Meteo_data = db.meteo_data
const Op = db.Sequelize.Op

exports.create = (req, res) => {
    console.log(req.body)
    if (!req.body.location_id) {
        res.status(400).send({ message: "location_id cannot be empty!" })
        return
    }

    const meteo_data = {
        location_id: req.body.location_id,
        timestamp_ws: req.body.timestamp_ws,
        wind_speed_knots: req.body.wind_speed_knots,
        wind_direction_deg: req.body.wind_direction_deg,
        barometric_pressure_ssl_hPa: req.body.barometric_pressure_ssl_hPa,
        rain_today_mm: req.body.rain_today_mm,
        rain_rate_mmh: req.body.rain_rate_mmh,
        temperature_cels: req.body.temperature_cels,
        rel_humidity: req.body.rel_humidity,
        uv_index: req.body.uv_index,
        heat_index_cels: req.body.heat_index_cels,
        wind_gust_knots: req.body.wind_gust_knots,
        dew_point_cels: req.body.dew_point_cels,
        wind_chill_cels: req.body.wind_chill_cels,
        ground_temperature_cels: req.body.ground_temperature_cels,
        solar_irradiance_wpsm: req.body.solar_irradiance_wpsm,
        rel_leaf_wetness: req.body.rel_leaf_wetness,
        soil_moisture_cb: req.body.soil_moisture_cb,
        rain_this_month_mm: req.body.rain_this_month_mm,
        rain_this_year_mm: req.body.rain_this_year_mm,
        evapotranspiration_today_mm: req.body.evapotranspiration_today_mm,
        evapotranspiration_this_month_mm: req.body.evapotranspiration_this_month_mm,
        evapotranspiration_this_year_mm: req.body.evapotranspiration_this_year_mm,
        perceived_temperature_cels: req.body.perceived_temperature_cels,
        humidex_cels: req.body.humidex_cels,
        wind_temperature_cels: req.body.wind_temperature_cels,
        current_weather: req.body.current_weather,
        wet_bulb_temperature_cels: req.body.wet_bulb_temperature_cels,
        absolute_humidity_gm3: req.body.absolute_humidity_gm3,
        saturated_vapor_pressure_hPa: req.body.saturated_vapor_pressure_hPa,
        windrun_km: req.body.windrun_km,
        barometric_pressure_wsl_hPa: req.body.barometric_pressure_wsl_hPa,
        average_wind_speed_knots: req.body.average_wind_speed_knots,
        storm_rain_mmm: req.body.storm_rain_mmm
    }

    Meteo_data.create(meteo_data)
        .then(data => { res.send(data) })
        .catch(err => {
            console.log(err.message)
            res.status(500).send({ message: err.message || "Some error occurred while creating Meteo_data record!" })
        })
}

exports.findAllByLocation = (req, res) => {
    const location_id = req.query.location_id
    var condition = location_id ? { location_id: { where: { location_id: location_id } } } : null
    Meteo_data.findAll({ where: condition })
        .then(data => { res.send(data) })
        .catch(err => { res.status(500).send({ message: err.message || `Some error occurred while retrieving Meteo_data records (location_id: ${location_id})!` }) })

}