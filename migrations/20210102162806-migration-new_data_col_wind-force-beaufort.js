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
                queryInterface.addColumn('meteo_data', 'wind_force_beaufort_desc', { type: Sequelize.STRING }, { transaction: t }),
                queryInterface.addColumn('ws_capabilities', 'wind_force_beaufort_desc', { type: Sequelize.BOOLEAN, defaultValue: false }, { transaction: t })
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
                queryInterface.removeColumn('meteo_data', 'wind_force_beaufort_desc', { transaction: t }),
                queryInterface.removeColumn('ws_capabilities', 'wind_force_beaufort_desc', { transaction: t })
            ]);
        });
    }
};