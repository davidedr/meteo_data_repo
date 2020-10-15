const db = require("../models")
const Meteo_data = db.meteo_data
const Op = db.Sequelize.Op

exports.create = (req, res) => {
    if (!req.body.location_id) {
        res.status(400).send({ message: "location_id cannot be empty!" })
        return
    }
    if (!req.body.location_id) {
        res.status(400).send({ message: "location_id cannot be empty!" })
        return
    }

    const meteo_data = {
        location_id: req.body.location_id,
        timestamp: req.body.timestamp,
        wind_speed_knots: req.body.wind_speed_knots,
        wind_direction_deg: req.body.wind_direction_deg,
        barometric_pressure_hPa: req.body.barometric_pressure_hPa,
        rain_today_mm: req.body.rain_today_mm,
        rain_rate_mmph: req.body.rain_rate_mmph,
        temperature_cels: req.body.temperature_cels,
        rel_humidity: req.body.rel_humidity,
        uv_index: req.body.uv_index,
        heat_index_cels: heat_index_cels.body.uv_index,
    }

    Meteo_data.create(meteo_data)
        .then(data => { res.send(data) })
        .catch(err => { res.status(500).send({ message: err.message || "Some error occurred while creating the Meteo_data record!" }) })
}

exports.findAllByLocation = (req, res) => {
    const location_id = req.query.location_id
    var condition = location_id ? { location_id: { where: { location_id: location_id } } } : null
    Meteo_data.findAll({ where: condition })
        .then(data => { res.send(data) })
        .catch(err => { res.status(500).send({ message: err.message || `Some error occurred while retrieving Meteo_data records (location_id: ${location_id})!` }) })

}