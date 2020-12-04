const db = require("../models")
const Ws_capabilities = db.ws_capabilities
const Op = db.Sequelize.Op

exports.create = (req, res) => {
    if (!req.body.location_id) {
        res.status(400).send({ message: "location id cannot be empty!" })
        return
    }

    const ws_capabilities = {
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
                res.status(404).send(`ws_capability id: ${id} not found!`)
            else
                res.send(data)
        })
        .catch(err => {
            res.status(500).send({
                message: err.message || `Some error occurred while retrieving Ws_capability: ${ id }!`
            })
        })

}

exports.findByLocationId = (req, res) => {
    const location_id = req.param('location_id')
    console.log(`findByLocationId, location_id: ${ location_id }...`)
    condition = { where: { location_id: location_id } }
    Ws_capabilities.findAll(condition)
        .then(data => {
            if (data.length == 0)
                res.status(404).send(`ws_capability location_id: ${ location_id } not found!`)
            else
                res.send(data)
        })
        .catch(err => {
            res.status(500).send({
                message: err.message || `Some error occurred while retrieving ws_capability location_id: ${ location_id }!`
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
    if (!ws_capabilities) {
        console.log("Not found")
        res.status(404).send(`Ws_capabilities: ${ id } not found!`)

    } else {

        const ws_capabilities = {
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
        }

        Ws_capabilities.update(values = ws_capabilities, options = { where: { id: id } })
            .then(data => { res.status(200).send("Update ok!") })
            .catch(err => { res.status(500).send({ message: err.message || `Some error occurred while updating Ws_capabilities record: ${ id }!` }) })
    }
}