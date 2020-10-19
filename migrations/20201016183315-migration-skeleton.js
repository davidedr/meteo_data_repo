'use strict';

const { QueryInterface } = require("sequelize/types");

module.exports = {
    up: async(queryInterface, Sequelize) => {
        return QueryInterface.sequelize.transaction(t => {
            return Promise.all([
                queryInterface.addColumn('meteo_data', 'wind_gust_knots', {
                    type: Sequelize.DECIMAL,
                    defaultValue: null,
                    validate: { min: 0 }
                }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'dew_point_cels', {
                    type: Sequelize.DECIMAL,
                    defaultValue: null,
                    validate: { min: -273.2, max: 273 }
                }, { transaction: t }),
            ])
        })

        /**
         * Add altering commands here.
         *
         * Example:
         * await queryInterface.createTable('users', { id: Sequelize.INTEGER });
         */
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
                queryInterface.removeColumn('meteo_data', 'wind_gust_knots', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'dew_point_cels', { transaction: t })
            ]);
        });
    }
};