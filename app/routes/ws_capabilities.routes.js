module.exports = app => {
    const ws_capabilities = require("../controllers/ws_capabilities.controller.js")
    var router = require("express").Router()

    router.post("/", ws_capabilities.create)
    router.get("/", ws_capabilities.findAll)
    router.get("/:id", ws_capabilities.findById)
    router.get("/location/:location_id", ws_capabilities.findByLocationId)
    router.patch("/:id", ws_capabilities.update)

    app.use('/api/ws_capabilities', router);
}