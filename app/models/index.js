const dbConfig = require("../config/db.config.js")
const Sequelize = require("sequelize")
const sequelize = new Sequelize(dbConfig.DB, dbConfig.USER, dbConfig.PASSWORD, {
    host: dbConfig.HOST,
    port: dbConfig.PORT,
    dialect: dbConfig.dialect,
    logging: dbConfig.logging,
    operatorAliases: false,
    pool: { max: dbConfig.max, min: dbConfig.min, acquire: dbConfig.pool.acquire, idle: dbConfig.pool.idle }
})

const db = {}
db.Sequelize = Sequelize
db.sequelize = sequelize
db.meteo_data = require("./meteo_data.model.js")(sequelize, Sequelize)
db.locations = require("./location.model.js")(sequelize, Sequelize)

module.exports = db