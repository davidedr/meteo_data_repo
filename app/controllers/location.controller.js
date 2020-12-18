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
        town: req.body.town,
        province: req.body.province,
        country: req.body.country,
        note: req.body.note,
        height_asl_m: req.body.height_asl_m
    }

    Locations.create(location)
        .then(data => { res.send(data) })
        .catch(err => { res.status(500).send({ message: err.message || "Some error occurred while creating Location record!" }) })
}

exports.findAll = (req, res) => {
    const name = req.param('name')
    condition = {}
    if (name)
        condition = {
            where: {
                name: {
                    [Op.like]: '%' + name + '%'
                }
            }
        }
    console.log(condition, { order: ['id'] })
    Locations.findAll(condition)
        .then(data => { res.send(data) })
        .catch(err => { res.status(500).send({ message: err.message || `Some error occurred while retrieving Location records!` }) })

}

exports.findById = (req, res) => {
    const id = req.param('id')
    condition = { where: { id: id } }
    Locations.findAll(condition)
        .then(data => { res.send(data) })
        .catch(err => {
            res.status(500).send({
                message: err.message || `Some error occurred while retrieving Location id: ${ id }!`
            })
        })

}

exports.update = (req, res) => {
    const id = req.params.id
    if (!id) {
        res.status(400).send({ message: "id cannot be empty!" })
        return
    }
    const location = Locations.findByPk(id)
    if (!location) {
        console.log("Not found")
        res.status(404).send(id)

    } else {
        const location_data = {
            name: req.body.name ? req.body.name : location.name,
            latitude: req.body.latitude ? req.body.latitude : location.latitude,
            longitude: req.body.longitude ? req.body.longitude : location.longitude,
            address_complete: req.body.address_complete ? req.body.address_complete : location.address_complete,
            street_1: req.body.street_1 ? req.body.street_1 : location.street_1,
            street_2: req.body.street_2 ? req.body.street_2 : location.street_2,
            zip: req.body.zip ? req.body.zip : location.zip,
            town: req.body.town ? req.body.town : location.town,
            province: req.body.province ? req.body.province : location.province,
            country: req.body.country ? req.body.country : location.country,
            note: req.body.note ? req.body.note : location.note,
            height_asl_m: req.body.height_asl_m ? req.body.height_asl_m : location.height_asl_m
        }

        Locations.update(values = location_data, options = { where: { id: id } })
            .then(data => { res.status(200).send("Update ok!") })
            .catch(err => { res.status(500).send({ message: err.message || `Some error occurred while updating Location record: ${ id }!` }) })
    }
}