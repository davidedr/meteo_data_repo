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
                queryInterface.addColumn('meteo_data', 'last_rain_event_timestamp', { type: Sequelize.DATE, allowNull: true, defaultValue: null }, { transaction: t })
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
                queryInterface.removeColumn('meteo_data', 'last_rain_event_timestamp', { transaction: t })
            ]);
        });
    }
};