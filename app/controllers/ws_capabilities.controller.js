const db = require("../models")
const Ws_capabilities = db.ws_capabilities
const Op = db.Sequelize.Op

exports.create = (req, res) => {
    if (!req.body.name) {
        res.status(400).send({ message: "location id cannot be empty!" })
        return
    }

    const ws_capabilities = {
        location_id: req.body.location_id,
        timestamp_ws: req.body.timestamp_ws ? req.body.timestamp_ws : ws_capabilities_data.timestamp_ws,
        wind_speed_knots: req.body.wind_speed_knots ? req.body.name : ws_capabilities_data.wind_speed_knots,
        wind_direction_deg: req.body.wind_direction_deg ? req.body.wind_direction_deg : ws_capabilities_data.wind_direction_deg,
        barometric_pressure_ssl_hPa: req.body.barometric_pressure_ssl_hPa ? req.body.name : ws_capabilities_data.barometric_pressure_ssl_hPa,
        rain_today_mm: req.body.rain_today_mm ? req.body.name : ws_capabilities_data.rain_today_mm,
        rain_rate_mmh: req.body.rain_rate_mmh ? req.body.rain_rate_mmh : ws_capabilities_data.rain_rate_mmh,
        temperature_cels: req.body.temperature_cels ? req.body.temperature_cels : ws_capabilities_data.temperature_cels,
        rel_humidity: req.body.rel_humidity ? req.body.rel_humidity : ws_capabilities_data.rel_humidity,
        uv_index: req.body.uv_index ? req.body.uv_index : ws_capabilities_data.uv_index,
        heat_index_cels: req.body.heat_index_cels ? req.body.heat_index_cels : ws_capabilities_data.heat_index_cels,
        wind_gust_knots: req.body.wind_gust_knots ? req.body.wind_gust_knots : ws_capabilities_data.wind_gust_knots,
        dew_point_cels: req.body.dew_point_cels ? req.body.dew_point_cels : ws_capabilities_data.dew_point_cels,
        wind_chill_cels: req.body.wind_chill_cels ? req.body.wind_chill_cels : ws_capabilities_data.wind_chill_cels,
        ground_temperature_cels: req.body.ground_temperature_cels ? req.body.ground_temperature_cels : ws_capabilities_data.ground_temperature_cels,
        solar_irradiance_wpsm: req.body.solar_irradiance_wpsm ? req.body.solar_irradiance_wpsm : ws_capabilities_data.solar_irradiance_wpsm,
        rel_leaf_wetness: req.body.rel_leaf_wetness ? req.body.rel_leaf_wetness : ws_capabilities_data.rel_leaf_wetness,
        soil_moisture_cb: req.body.soil_moisture_cb ? req.body.soil_moisture_cb : ws_capabilities_data.soil_moisture_cb,
        rain_this_month_mm: req.body.rain_this_month_mm ? req.body.rain_this_month_mm : ws_capabilities_data.rain_this_month_mm,
        rain_this_year_mm: req.body.rain_this_year_mm ? req.body.rain_this_year_mm : ws_capabilities_data.rain_this_year_mm,
        evapotranspiration_this_month_mm: req.body.evapotranspiration_this_month_mm ? req.body.evapotranspiration_this_month_mm : ws_capabilities_data.evapotranspiration_this_month_mm,
        evapotranspiration_this_year_mm: req.body.evapotranspiration_this_year_mm ? req.body.evapotranspiration_this_year_mm : ws_capabilities_data.evapotranspiration_this_year_mm,
        perceived_temperature_cels: req.body.perceived_temperature_cels ? req.body.perceived_temperature_cels : ws_capabilities_data.perceived_temperature_cels,
        humidex_cels: req.body.humidex_cels ? req.body.humidex_cels : ws_capabilities_data.humidex_cels,
        wind_temperature_cels: req.body.wind_temperature_cels ? req.body.wind_temperature_cels : ws_capabilities_data.wind_temperature_cels,
        current_weather: req.body.current_weather ? req.body.current_weather : ws_capabilities_data.current_weather,
        wet_bulb_temperature_cels: req.body.wet_bulb_temperature_cels ? req.body.wet_bulb_temperature_cels : ws_capabilities_data.wet_bulb_temperature_cels,
        absolute_humidity_gm3: req.body.absolute_humidity_gm3 ? req.body.absolute_humidity_gm3 : ws_capabilities_data.absolute_humidity_gm3,
        saturated_vapor_pressure_hPa: req.body.saturated_vapor_pressure_hPa ? req.body.saturated_vapor_pressure_hPa : ws_capabilities_data.saturated_vapor_pressure_hPa,
        windrun_km: req.body.windrun_km ? req.body.windrun_km : ws_capabilities_data.windrun_km,
        barometric_pressure_wsl_hPa: req.body.barometric_pressure_wsl_hPa ? req.body.barometric_pressure_wsl_hPa : ws_capabilities_data.barometric_pressure_wsl_hPa,
        average_wind_speed_knots: req.body.average_wind_speed_knots ? req.body.average_wind_speed_knots : ws_capabilities_data.average_wind_speed_knots,
        storm_rain_mmm: req.body.storm_rain_mmm ? req.body.storm_rain_mmm : ws_capabilities_data.storm_rain_mmm,
        rain_in_last_storm_event_mm: req.body.rain_in_last_storm_event_mm ? req.body.rain_in_last_storm_event_mm : ws_capabilities_data.rain_in_last_storm_event_mm,
        rain_in_last_storm_event_mm: req.body.cloud_height_m ? req.body.cloud_height_m : ws_capabilities_data.cloud_height_m

    }

    Ws_capabilities.create(ws_capabilities)
        .then(data => { res.send(data) })
        .catch(err => { res.status(500).send({ message: err.message || "Some error occurred while creating Ws_capabilities record!" }) })

}

exports.findAll = (req, res) => {
    Ws_capabilities.findAll({ order: ['id'] })
        .then(data => { res.send(data) })
        .catch(err => { res.status(500).send({ message: err.message || `Some error occurred while retrieving Ws_capabilities records!` }) })

}

exports.findById = (req, res) => {
    const id = req.param('id')
    condition = { where: { id: id } }
    Ws_capabilities.findAll(condition)
        .then(data => {
            if (data.length == 0)
                res.status(404)
            else
                res.send(data)
        })
        .catch(err => {
            res.status(500).send({
                message: err.message || `Some error occurred while retrieving Ws_capability: ${ id }!`
            })
        })

}

exports.update = (req, res) => {
    const id = req.params.id
    if (!id) {
        res.status(400).send({ message: "id cannot be empty!" })
        return
    }
    const ws_capabilities = Ws_capabilities.findByPk(id)
    if (!ws_capabilities_data) {
        console.log("Not found")
        res.status(404).send(`Ws_capabilities: ${ id } not found!`)

    } else {

        const ws_capabilities_data = {
            timestamp_ws: req.body.timestamp_ws ? req.body.timestamp_ws : ws_capabilities_data.timestamp_ws,
            wind_speed_knots: req.body.wind_speed_knots ? req.body.name : ws_capabilities_data.wind_speed_knots,
            wind_direction_deg: req.body.wind_direction_deg ? req.body.wind_direction_deg : ws_capabilities_data.wind_direction_deg,
            barometric_pressure_ssl_hPa: req.body.barometric_pressure_ssl_hPa ? req.body.name : ws_capabilities_data.barometric_pressure_ssl_hPa,
            rain_today_mm: req.body.rain_today_mm ? req.body.name : ws_capabilities_data.rain_today_mm,
            rain_rate_mmh: req.body.rain_rate_mmh ? req.body.rain_rate_mmh : ws_capabilities_data.rain_rate_mmh,
            temperature_cels: req.body.temperature_cels ? req.body.temperature_cels : ws_capabilities_data.temperature_cels,
            rel_humidity: req.body.rel_humidity ? req.body.rel_humidity : ws_capabilities_data.rel_humidity,
            uv_index: req.body.uv_index ? req.body.uv_index : ws_capabilities_data.uv_index,
            heat_index_cels: req.body.heat_index_cels ? req.body.heat_index_cels : ws_capabilities_data.heat_index_cels,
            wind_gust_knots: req.body.wind_gust_knots ? req.body.wind_gust_knots : ws_capabilities_data.wind_gust_knots,
            dew_point_cels: req.body.dew_point_cels ? req.body.dew_point_cels : ws_capabilities_data.dew_point_cels,
            wind_chill_cels: req.body.wind_chill_cels ? req.body.wind_chill_cels : ws_capabilities_data.wind_chill_cels,
            ground_temperature_cels: req.body.ground_temperature_cels ? req.body.ground_temperature_cels : ws_capabilities_data.ground_temperature_cels,
            solar_irradiance_wpsm: req.body.solar_irradiance_wpsm ? req.body.solar_irradiance_wpsm : ws_capabilities_data.solar_irradiance_wpsm,
            rel_leaf_wetness: req.body.rel_leaf_wetness ? req.body.rel_leaf_wetness : ws_capabilities_data.rel_leaf_wetness,
            soil_moisture_cb: req.body.soil_moisture_cb ? req.body.soil_moisture_cb : ws_capabilities_data.soil_moisture_cb,
            rain_this_month_mm: req.body.rain_this_month_mm ? req.body.rain_this_month_mm : ws_capabilities_data.rain_this_month_mm,
            rain_this_year_mm: req.body.rain_this_year_mm ? req.body.rain_this_year_mm : ws_capabilities_data.rain_this_year_mm,
            evapotranspiration_this_month_mm: req.body.evapotranspiration_this_month_mm ? req.body.evapotranspiration_this_month_mm : ws_capabilities_data.evapotranspiration_this_month_mm,
            evapotranspiration_this_year_mm: req.body.evapotranspiration_this_year_mm ? req.body.evapotranspiration_this_year_mm : ws_capabilities_data.evapotranspiration_this_year_mm,
            perceived_temperature_cels: req.body.perceived_temperature_cels ? req.body.perceived_temperature_cels : ws_capabilities_data.perceived_temperature_cels,
            humidex_cels: req.body.humidex_cels ? req.body.humidex_cels : ws_capabilities_data.humidex_cels,
            wind_temperature_cels: req.body.wind_temperature_cels ? req.body.wind_temperature_cels : ws_capabilities_data.wind_temperature_cels,
            current_weather: req.body.current_weather ? req.body.current_weather : ws_capabilities_data.current_weather,
            wet_bulb_temperature_cels: req.body.wet_bulb_temperature_cels ? req.body.wet_bulb_temperature_cels : ws_capabilities_data.wet_bulb_temperature_cels,
            absolute_humidity_gm3: req.body.absolute_humidity_gm3 ? req.body.absolute_humidity_gm3 : ws_capabilities_data.absolute_humidity_gm3,
            saturated_vapor_pressure_hPa: req.body.saturated_vapor_pressure_hPa ? req.body.saturated_vapor_pressure_hPa : ws_capabilities_data.saturated_vapor_pressure_hPa,
            windrun_km: req.body.windrun_km ? req.body.windrun_km : ws_capabilities_data.windrun_km,
            barometric_pressure_wsl_hPa: req.body.barometric_pressure_wsl_hPa ? req.body.barometric_pressure_wsl_hPa : ws_capabilities_data.barometric_pressure_wsl_hPa,
            average_wind_speed_knots: req.body.average_wind_speed_knots ? req.body.average_wind_speed_knots : ws_capabilities_data.average_wind_speed_knots,
            storm_rain_mmm: req.body.storm_rain_mmm ? req.body.storm_rain_mmm : ws_capabilities_data.storm_rain_mmm,
            rain_in_last_storm_event_mm: req.body.rain_in_last_storm_event_mm ? req.body.rain_in_last_storm_event_mm : ws_capabilities_data.rain_in_last_storm_event_mm,
            rain_in_last_storm_event_mm: req.body.cloud_height_m ? req.body.cloud_height_m : ws_capabilities_data.cloud_height_m

        }

        Ws_capabilities.update(values = ws_capabilities_data, options = { where: { id: id } })
            .then(data => { res.status(200).send("Update ok!") })
            .catch(err => { res.status(500).send({ message: err.message || `Some error occurred while updating Ws_capabilities record: ${ id }!` }) })
    }
}