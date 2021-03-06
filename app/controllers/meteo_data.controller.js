const db = require("../models")
const Meteo_data = db.meteo_data
const Op = db.Sequelize.Op
const logger = require('winston')

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
        storm_rain_mmm: req.body.storm_rain_mmm,
        rain_in_last_storm_event_mm: req.body.rain_in_last_storm_event_mm,
        cloud_height_m: req.body.cloud_height_m,
        air_density_kgm3: req.body.air_density_kgm3,
        rel_equilibrium_moisture_content: req.body.rel_equilibrium_moisture_content,
        wind_force_beaufort_desc: req.body.wind_force_beaufort_desc,
        moon_phase_desc: req.body.moon_phase_desc,
        sunrise_timestamp: req.body.sunrise_timestamp,
        sunset_timestamp: req.body.sunset_timestamp,
        last_rain_event_timestamp: req.body.last_rain_event_timestamp
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

exports.getMeta = (req, res) => {
    data = {
        timestamp_ws: "timestamp_ws",
        wind_speed_knots: "wind_speed_knots",
        wind_direction_deg: "wind_direction_deg",
        barometric_pressure_ssl_hPa: "barometric_pressure_ssl_hPa",
        rain_today_mm: "rain_today_mm",
        rain_rate_mmh: "rain_rate_mmh",
        temperature_cels: "temperature_cels",
        rel_humidity: "rel_humidity",
        uv_index: "uv_index",
        heat_index_cels: "heat_index_cels",
        wind_gust_knots: "wind_gust_knots",
        dew_point_cels: "dew_point_cels",
        wind_chill_cels: "wind_chill_cels",
        ground_temperature_cels: "ground_temperature_cels",
        solar_irradiance_wpsm: "solar_irradiance_wpsm",
        rel_leaf_wetness: "rel_leaf_wetness",
        soil_moisture_cb: "soil_moisture_cb",
        rain_this_month_mm: "rain_this_month_mm",
        rain_this_year_mm: "rain_this_year_mm",
        evapotranspiration_today_mm: "evapotranspiration_today_mm",
        evapotranspiration_this_month_mm: "evapotranspiration_this_month_mm",
        evapotranspiration_this_year_mm: "evapotranspiration_this_year_mm",
        perceived_temperature_cels: "perceived_temperature_cels",
        humidex_cels: "humidex_cels",
        wind_temperature_cels: "wind_temperature_cels",
        current_weather: "current_weather",
        wet_bulb_temperature_cels: "wet_bulb_temperature_cels",
        absolute_humidity_gm3: "absolute_humidity_gm3",
        saturated_vapor_pressure_hPa: "saturated_vapor_pressure_hPa",
        windrun_km: "windrun_km",
        barometric_pressure_wsl_hPa: "barometric_pressure_wsl_hPa",
        average_wind_speed_knots: "req.body.average_wind_speed_kno",
        storm_rain_mmm: "storm_rain_mmm",
        rain_in_last_storm_event_mm: "rain_in_last_storm_event_mm",
        cloud_height_m: "cloud_height_m",
        air_density_kgm3: "air_density_kgm3",
        equilibrium_moisture_content: "equilibrium_moisture_content",
        wind_force_beaufort_desc: "wind_force_beaufort_desc",
        moon_phase_desc: "moon_phase_desc",
        sunrise_timestamp: "sunrise_timestamp",
        sunset_timestamp: "sunset_timestamp",
        last_rain_event_timestamp: "last_rain_event_timestamp"
    }
    res.status(200).send(data)

}