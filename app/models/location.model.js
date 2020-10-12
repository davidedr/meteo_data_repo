// Thanks to MANUEL RAUBER for points handling. See:
// https://manuel-rauber.com/2016/01/08/using-geo-based-data-with-sequelizejs-utilizing-postgresql-and-ms-sql-server-in-node-js/

module.exports = (sequelize, Sequelize) => {
    const location = sequelize.define("location", {
        id: { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true },
        name: { type: Sequelize.STRING, allowNull: false },
        latitude: { type: Sequelize.INTEGER, allowNull: true, defaultValue: null, validate: { min: -90, max: 90 } },
        longitude: { type: Sequelize.INTEGER, allowNull: true, defaultValue: null, validate: { min: -180, max: 180 } },
        address_complete: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        street_1: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        street_2: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        zip: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        province: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        country: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        note: { type: Sequelize.STRING, allowNull: true, defaultValue: null }
    })
}