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
                queryInterface.bulkInsert('ws_capabilities', [{
                        location_id: 1,
                        timestamp_ws: true,
                        wind_speed_knots: true,
                        wind_direction_deg: true,
                        barometric_pressure_ssl_hPa: true,
                        rain_today_mm: true,
                        rain_rate_mmh: true,
                        temperature_cels: true,
                        rel_humidity: true,
                        uv_index: true,
                        heat_index_cels: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 4,
                        timestamp_ws: true,
                        wind_speed_knots: true,
                        wind_gust_knots: true,
                        wind_direction_deg: true,
                        barometric_pressure_ssl_hPa: true,
                        rain_today_mm: true,
                        rain_rate_mmh: true,
                        temperature_cels: true,
                        rel_humidity: true,
                        perceived_temperature_cels: true,
                        dew_point_cels: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 8,
                        timestamp_ws: true,
                        wind_speed_knots: true,
                        wind_gust_knots: true,
                        wind_direction_deg: true,
                        barometric_pressure_ssl_hPa: true,
                        rain_today_mm: true,
                        rain_rate_mmh: true,
                        temperature_cels: true,
                        rel_humidity: true,
                        perceived_temperature_cels: true,
                        dew_point_cels: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 9,
                        timestamp_ws: true,
                        wind_speed_knots: true,
                        wind_gust_knots: true,
                        wind_direction_deg: true,
                        barometric_pressure_ssl_hPa: true,
                        rain_today_mm: true,
                        rain_rate_mmh: true,
                        temperature_cels: true,
                        rel_humidity: true,
                        perceived_temperature_cels: true,
                        dew_point_cels: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 10,
                        timestamp_ws: true,
                        wind_speed_knots: true,
                        wind_gust_knots: true,
                        wind_direction_deg: true,
                        barometric_pressure_ssl_hPa: true,
                        rain_today_mm: true,
                        rain_rate_mmh: true,
                        temperature_cels: true,
                        rel_humidity: true,
                        perceived_temperature_cels: true,
                        dew_point_cels: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 11,
                        timestamp_ws: true,
                        temperature_cels: true,
                        rel_humidity: true,
                        barometric_pressure_ssl_hPa: true,
                        wind_speed_knots: true,
                        wind_gust_knots: true,
                        wind_direction_deg: true,
                        rain_today_mm: true,
                        dew_point_cels: true,
                        heat_index_cels: true,
                        solar_irradiance_wpsm: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 12,
                        timestamp_ws: true,
                        wind_speed_knots: true,
                        average_wind_speed_knots: true,
                        wind_gust_knots: true,
                        wind_direction_deg: true,
                        barometric_pressure_ssl_hPa: true,
                        rain_today_mm: true,
                        rain_rate_mmh: true,
                        temperature_cels: true,
                        rel_humidity: true,
                        heat_index_cels: true,
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
                        rain_in_last_storm_event_mm: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 15,
                        timestamp_ws: true,
                        barometric_pressure_ssl_hPa: true,
                        rain_today_mm: true,
                        rain_rate_mmh: true,
                        rain_this_month_mm: true,
                        rain_this_year_mm: true,
                        storm_rain_mmm: true,
                        rel_humidity: true,
                        humidex_cels: true,
                        current_weather: true,
                        temperature_cels: true,
                        perceived_temperature_cels: true,
                        dew_point_cels: true,
                        wind_temperature_cels: true,
                        average_wind_speed_knots: true,
                        wet_bulb_temperature_cels: true,
                        wind_speed_knots: true,
                        wind_gust_knots: true,
                        wind_direction_deg: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 16,
                        timestamp_ws: true,
                        barometric_pressure_ssl_hPa: true,
                        rain_today_mm: true,
                        rain_rate_mmh: true,
                        rain_this_month_mm: true,
                        rain_this_year_mm: true,
                        storm_rain_mmm: true,
                        rel_humidity: true,
                        humidex_cels: true,
                        current_weather: true,
                        temperature_cels: true,
                        perceived_temperature_cels: true,
                        dew_point_cels: true,
                        wind_temperature_cels: true,
                        average_wind_speed_knots: true,
                        wet_bulb_temperature_cels: true,
                        wind_speed_knots: true,
                        wind_gust_knots: true,
                        wind_direction_deg: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 17,
                        timestamp_ws: true,
                        temperature_cels: true,
                        rel_humidity: true,
                        barometric_pressure_ssl_hPa: true,
                        wind_speed_knots: true,
                        wind_gust_knots: true,
                        wind_direction_deg: true,
                        rain_today_mm: true,
                        dew_point_cels: true,
                        heat_index_cels: true,
                        solar_irradiance_wpsm: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 18,
                        timestamp_ws: true,
                        temperature_cels: true,
                        perceived_temperature_cels: true,
                        humidex_cels: true,
                        rel_humidity: true,
                        absolute_humidity_gm3: true,
                        saturated_vapor_pressure_hPa: true,
                        barometric_pressure_ssl_hPa: true,
                        barometric_pressure_wsl_hPa: true,
                        wind_speed_knots: true,
                        wind_direction_deg: true,
                        wind_gust_knots: true,
                        windrun_km: true,
                        rain_rate_mmh: true,
                        rain_today_mm: true,
                        rain_this_month_mm: true,
                        rain_this_year_mm: true,
                        dew_point_cels: true,
                        wind_chill_cels: true,
                        wet_bulb_temperature_cels: true,
                        uv_index: true,
                        heat_index_cels: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    },
                    {
                        location_id: 19,
                        timestamp_ws: true,
                        wind_speed_knots: true,
                        wind_direction_deg: true,
                        barometric_pressure_ssl_hPa: true,
                        barometric_pressure_wsl_hPa: true,
                        rain_today_mm: true,
                        rain_rate_mmh: true,
                        temperature_cels: true,
                        rel_humidity: true,
                        uv_index: true,
                        wind_gust_knots: true,
                        wind_chill_cels: true,
                        solar_irradiance_wpsm: true,
                        cloud_height_m: true,
                        rain_this_month_mm: true,
                        rain_this_year_mm: true,
                        evapotranspiration_today_mm: true,
                        perceived_temperature_cels: true,
                        wet_bulb_temperature_cels: true,
                        average_wind_speed_knots: true,
                        createdAt: Sequelize.fn('now'),
                        updatedAt: Sequelize.fn('now')
                    }
                ], { transaction: t })
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
        return queryInterface.sequelize.transaction(t => {
            return Promise.all([
                queryInterface.bulkDelete('ws_capabilities', [
                    { id: 1 }, { id: 4 }, { id: 8 }, { id: 9 }, { id: 10 }, { id: 11 },
                    { id: 12 }, { id: 15 }, { id: 16 }, { id: 17 }, { id: 18 }, { id: 19 }
                ], { transaction: t })
            ])
        })
    }
}