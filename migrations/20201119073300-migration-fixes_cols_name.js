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
                queryInterface.renameColumn('meteo_data', 'barometric_pressure_hPa', 'barometric_pressure_ssl_hPa'), // Standard Sea Level
                queryInterface.renameColumn('meteo_data', 'rain_rate_mmph', 'rain_rate_mmh'),
                queryInterface.renameColumn('meteo_data', 'wind_Temperature_cels', 'wind_temperature_cels'),
                queryInterface.renameColumn('meteo_data', 'wind_travel_km', 'windrun_km'),
                queryInterface.renameColumn('meteo_data', 'ws_level_barometric_pressure_mPa', 'barometric_pressure_wsl_hPa') // Weather Station Level

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
                queryInterface.renameColumn('meteo_data', 'barometric_pressure_ssl_hPa', 'barometric_pressure_hPa'),
                queryInterface.renameColumn('meteo_data', 'rain_rate_mmh', 'rain_rate_mmph'),
                queryInterface.renameColumn('meteo_data', 'wind_temperature_cels', 'wind_Temperature_cels'),
                queryInterface.renameColumn('meteo_data', 'windrun_km', 'wind_travel_km'),
                queryInterface.renameColumn('meteo_data', 'barometric_pressure_wsl_hPa', 'ws_level_barometric_pressure_mPa')
            ])
        })
    }
};