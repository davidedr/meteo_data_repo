module.exports = app => {
    const ws_capabilities = require("../controllers/ws_capabilities.controller.js")
    var router = require("express").Router()

    router.get("/", ws_capabilities.findAll)
    router.get("/:id", ws_capabilities.findById)
    router.patch("/:id", ws_capabilities.update)

    app.use('/api/ws_capabilities', router);
}