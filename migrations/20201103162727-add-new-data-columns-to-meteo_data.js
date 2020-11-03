'use strict';

module.exports = {
    up: async(queryInterface, Sequelize) => {
        /**
         * Add altering commands here.
         *
         * Example:
         * await queryInterface.createTable('users', { id: Sequelize.INTEGER });
         */
        return queryInterface.sequelize.transaction(t => {
            return Promise.all([
                queryInterface.addColumn('meteo_data', 'wind_chill_cels', { type: Sequelize.DECIMAL, validate: { min: -273.2, max: 273 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'ground_temperature_cels', { type: Sequelize.DECIMAL, validate: { min: -273.2, max: 273 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'solar_irradiance_wpsm', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'rel_leaf_wetness', { type: Sequelize.DECIMAL, validate: { min: 0, max: 1 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'soil_moisture_cb', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'rain_this_month_mm', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'rain_this_year_mm', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'evapotranspiration_today_mm', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'evapotranspiration_this_month_mm', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'evapotranspiration_this_year_mm', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t })
            ])
        })
    },

    down: async(queryInterface, Sequelize) => {
        /**
         * Add reverting commands here.
         *
         * Example:
         * await queryInterface.dropTable('users');
         */
        return queryInterface.sequelize.transaction(t => {
            return Promise.all([
                queryInterface.removeColumn('meteo_data', 'wind_chill_cels', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'ground_temperature_cels', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'solar_irradiance_wpsm', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'rel_leaf_wetness', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'soil_moisture_cb', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'rain_this_month_mm', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'rain_this_year_mm', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'evapotranspiration_today_mm', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'evapotranspiration_this_month_mm', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'evapotranspiration_this_year_mm', { transaction: t })
            ]);
        });
    }
};