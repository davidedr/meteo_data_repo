const db = require("../models")
const Locations = db.locations
const Op = db.Sequelize.Op

exports.create = (req, res) => {
    if (!req.body.name) {
        res.status(400).send({ message: "name cannot be empty!" })
        return
    }

    const location = {
        name: req.body.name,
        latitude: req.body.latitude,
        longitude: req.body.longitude,
        address_complete: req.body.address_complete,
        street_1: req.body.street_1,
        street_2: req.body.street_2,
        zip: req.body.zip,
        province: req.body.province,
        country: req.body.country,
        note: req.body.note
    }

    Locations.create(location)
        .then(data => { res.send(data) })
        .catch(err => { res.status(500).send({ message: err.message || "Some error occurred while creating Location record!" }) })
}

exports.findAll = (req, res) => {
    Locations.findAll()
        .then(data => { res.send(data) })
        .catch(err => { res.status(500).send({ message: err.message || `Some error occurred while retrieving Location records!` }) })

}