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
                queryInterface.bulkUpdate('ws_capabilities', {
                    timestamp_ws: true,
                    wind_speed_knots: true,
                    wind_direction_deg: true,
                    barometric_pressure_ssl_hPa: true,
                    rain_today_mm: true,
                    rain_rate_mmh: true,
                    temperature_cels: true,
                    rel_humidity: true,
                    heat_index_cels: true,
                    wind_gust_knots: true,
                    dew_point_cels: true,
                    wind_chill_cels: true,
                    ground_temperature_cels: true,
                    solar_irradiance_wpsm: true,
                    rel_leaf_wetness: true,
                    soil_moisture_cb: true,
                    rain_this_month_mm: true,
                    rain_this_year_mm: true,
                    evapotranspiration_today_mm: true,
                    evapotranspiration_this_month_mm: true,
                    evapotranspiration_this_year_mm: true,
                    perceived_temperature_cels: true,
                    average_wind_speed_knots: true,
                    rain_in_last_storm_event_mm: true,
                    air_density_kgm3: true,
                    rel_equilibrium_moisture_content: true
                }, { location_id: 21 }, { transaction: t })
            ]);
        });
    },

    down: async(queryInterface, Sequelize) => {
        /**
         * Add reverting commands here.
         *
         * Example:
         * await queryInterface.dropTable('users');
         */
    }
};