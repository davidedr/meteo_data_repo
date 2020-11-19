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
                queryInterface.addColumn('meteo_data', 'perceived_temperature_cels', { type: Sequelize.DECIMAL, validate: { min: -273.2, max: 273 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'humidex_cels', { type: Sequelize.DECIMAL, validate: { min: -273.2, max: 273 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'wind_Temperature_cels', { type: Sequelize.DECIMAL, validate: { min: -273.2, max: 273 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'current_weather', { type: Sequelize.STRING }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'wet_bulb_temperature_cels', { type: Sequelize.DECIMAL, validate: { min: -273.2, max: 273 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'absolute_humidity_gm3', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'saturated_vapor_pressure_hPa', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'wind_travel_km', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'ws_level_barometric_pressure_mPa', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'average_wind_speed_knots', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t })
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
                queryInterface.removeColumn('meteo_data', 'winperceived_temperature_celsd_chill_cels', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'humidex_cels', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'wind_Temperature_cels', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'current_weather', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'wet_bulb_temperature_cels', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'absolute_humidity_gm3', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'saturated_vapor_pressure_hPa', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'wind_travel_km', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'ws_level_barometric_pressure_mPa', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'average_wind_speed_knots', { transaction: t })
            ]);
        });
    }
};