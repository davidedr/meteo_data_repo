module.exports = app => {
    const location = require("../controllers/location.controller.js")
    var router = require("express").Router()

    router.post("/", location.create)
    router.get("/", location.findAll)
    router.get("/:id", location.findById)
    app.use('/api/location', router);
}