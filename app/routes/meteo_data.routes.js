module.exports = app => {
    const meteo_data = require("../controllers/meteo_data.controller.js")
    var router = require("express").Router()

    router.post("/", meteo_data.create)
    router.get("/", meteo_data.findAllByLocation)
    router.get("/meta", meteo_data.getMeta)

    app.use('/api/meteo_data', router);
}