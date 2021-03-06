// Thanks to MANUEL RAUBER for points handling. See:
// https://manuel-rauber.com/2016/01/08/using-geo-based-data-with-sequelizejs-utilizing-postgresql-and-ms-sql-server-in-node-js/

module.exports = (sequelize, Sequelize) => {
    const Location = sequelize.define("location", {
        id: { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true },
        name: { type: Sequelize.STRING, allowNull: false },
        latitude: { type: Sequelize.DECIMAL, allowNull: true, defaultValue: null, validate: { min: -90, max: 90 } },
        longitude: { type: Sequelize.DECIMAL, allowNull: true, defaultValue: null, validate: { min: -180, max: 180 } },
        address_complete: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        street_1: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        street_2: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        zip: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        town: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        province: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        country: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        note: { type: Sequelize.STRING, allowNull: true, defaultValue: null },
        height_asl_m: { type: Sequelize.DECIMAL, allowNull: true, defaultValue: null, validate: { min: 0 } }
    })

    Location.associate = function(models) {
        Location.hasOne(models.ws_capabilities, { foreignKey: 'location_id', as: 'ws_capabilities', onDelete: 'CASCADE' });
    }

    return Location
}