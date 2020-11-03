module.exports = (sequelize, Sequelize) => {
    const Meteo_data = sequelize.define("meteo_data", {
        id: { type: Sequelize.INTEGER, primaryKey: true, autoIncrement: true },
        location_id: { type: Sequelize.INTEGER },
        timestamp_ws: { type: Sequelize.DATE, defaultValue: Sequelize.NOW },
        wind_speed_knots: { type: Sequelize.DECIMAL, defaultValue: null, validate: { min: 0 } },
        wind_direction_deg: { type: Sequelize.DECIMAL, defaultValue: null, validate: { min: 0, max: 359 } },
        barometric_pressure_hPa: { type: Sequelize.DECIMAL, defaultValue: null, validate: { min: 0 } },
        rain_today_mm: { type: Sequelize.DECIMAL, defaultValue: null, validate: { min: 0 } },
        rain_rate_mmph: { type: Sequelize.DECIMAL, defaultValue: null, validate: { min: 0 } },
        temperature_cels: { type: Sequelize.DECIMAL, defaultValue: null, validate: { min: -273.2, max: 273 } },
        rel_humidity: { type: Sequelize.DECIMAL, defaultValue: null, validate: { min: 0, max: 1 } },
        uv_index: { type: Sequelize.DECIMAL, defaultValue: null, validate: { min: 0 } },
        heat_index_cels: { type: Sequelize.DECIMAL, defaultValue: null },
        wind_gust_knots: { type: Sequelize.DECIMAL, defaultValue: null, validate: { min: 0 } },
        dew_point_cels: { type: Sequelize.DECIMAL, defaultValue: null, validate: { min: -273.2, max: 273 } },
        wind_chill_cels: { type: Sequelize.DECIMAL, validate: { min: -273.2, max: 273 } },
        ground_temperature_cels: { type: Sequelize.DECIMAL, validate: { min: -273.2, max: 273 } },
        solar_irradiance_wpsm: { type: Sequelize.DECIMAL, validate: { min: 0 } },
        rel_leaf_wetness: { type: Sequelize.DECIMAL, validate: { min: 0, max: 1 } },
        soil_moisture_cb: { type: Sequelize.DECIMAL, validate: { min: 0 } },
        rain_this_month_mm: { type: Sequelize.DECIMAL, validate: { min: 0 } },
        rain_this_year_mm: { type: Sequelize.DECIMAL, validate: { min: 0 } },
        evapotranspiration_today_mm: { type: Sequelize.DECIMAL, validate: { min: 0 } },
        evapotranspiration_this_month_mm: { type: Sequelize.DECIMAL, validate: { min: 0 } },
        evapotranspiration_this_year_mm: { type: Sequelize.DECIMAL, validate: { min: 0 } }
    })

    return Meteo_data
}