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
                queryInterface.createTable('ws_capabilities', {
                    id: { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true },
                    location_id: { type: Sequelize.INTEGER, references: { model: 'locations', key: 'id' }, onDelete: 'cascade' },
                    timestamp_ws: { type: Sequelize.BOOLEAN, defaultValue: false },
                    wind_speed_knots: { type: Sequelize.BOOLEAN, defaultValue: false },
                    wind_direction_deg: { type: Sequelize.BOOLEAN, defaultValue: false },
                    barometric_pressure_ssl_hPa: { type: Sequelize.BOOLEAN, defaultValue: false },
                    rain_today_mm: { type: Sequelize.BOOLEAN, defaultValue: false },
                    rain_rate_mmh: { type: Sequelize.BOOLEAN, defaultValue: false },
                    temperature_cels: { type: Sequelize.BOOLEAN, defaultValue: false },
                    rel_humidity: { type: Sequelize.BOOLEAN, defaultValue: false },
                    uv_index: { type: Sequelize.BOOLEAN, defaultValue: false },
                    heat_index_cels: { type: Sequelize.BOOLEAN, defaultValue: false },
                    wind_gust_knots: { type: Sequelize.BOOLEAN, defaultValue: false },
                    dew_point_cels: { type: Sequelize.BOOLEAN, defaultValue: false },
                    wind_chill_cels: { type: Sequelize.BOOLEAN, defaultValue: false },
                    ground_temperature_cels: { type: Sequelize.BOOLEAN, defaultValue: false },
                    solar_irradiance_wpsm: { type: Sequelize.BOOLEAN, defaultValue: false },
                    rel_leaf_wetness: { type: Sequelize.BOOLEAN, defaultValue: false },
                    soil_moisture_cb: { type: Sequelize.BOOLEAN, defaultValue: false },
                    rain_this_month_mm: { type: Sequelize.BOOLEAN, defaultValue: false },
                    rain_this_year_mm: { type: Sequelize.BOOLEAN, defaultValue: false },
                    evapotranspiration_today_mm: { type: Sequelize.BOOLEAN, defaultValue: false },
                    evapotranspiration_this_month_mm: { type: Sequelize.BOOLEAN, defaultValue: false },
                    evapotranspiration_this_year_mm: { type: Sequelize.BOOLEAN, defaultValue: false },
                    perceived_temperature_cels: { type: Sequelize.BOOLEAN, defaultValue: false },
                    humidex_cels: { type: Sequelize.BOOLEAN, defaultValue: false },
                    wind_temperature_cels: { type: Sequelize.BOOLEAN, defaultValue: false },
                    current_weather: { type: Sequelize.BOOLEAN, defaultValue: false },
                    wet_bulb_temperature_cels: { type: Sequelize.BOOLEAN, defaultValue: false },
                    absolute_humidity_gm3: { type: Sequelize.BOOLEAN, defaultValue: false },
                    saturated_vapor_pressure_hPa: { type: Sequelize.BOOLEAN, defaultValue: false },
                    windrun_km: { type: Sequelize.BOOLEAN, defaultValue: false },
                    barometric_pressure_wsl_hPa: { type: Sequelize.BOOLEAN, defaultValue: false },
                    average_wind_speed_knots: { type: Sequelize.BOOLEAN, defaultValue: false },
                    storm_rain_mmm: { type: Sequelize.BOOLEAN, defaultValue: false },
                    rain_in_last_storm_event_mm: { type: Sequelize.BOOLEAN, defaultValue: false },
                    cloud_height_m: { type: Sequelize.BOOLEAN, defaultValue: false }
                }, { transaction: t })
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
                queryInterface.dropTable('ws_capabilities', { transaction: t })
            ]);
        });
    }
};