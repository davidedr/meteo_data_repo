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
                queryInterface.addColumn('meteo_data', 'air_density_kgm3', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('ws_capabilities', 'air_density_kgm3', { type: Sequelize.BOOLEAN, defaultValue: false }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'equilibrium_moisture_content', { type: Sequelize.DECIMAL, validate: { min: 0 } }, { transaction: t }),
                queryInterface.addColumn('ws_capabilities', 'equilibrium_moisture_content', { type: Sequelize.BOOLEAN, defaultValue: false }, { transaction: t })
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
                queryInterface.removeColumn('meteo_data', 'air_density_kgm3', { transaction: t }),
                queryInterface.removeColumn('ws_capabilities', 'air_density_kgm3', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'equilibrium_moisture_content', { transaction: t }),
                queryInterface.removeColumn('ws_capabilities', 'equilibrium_moisture_content', { transaction: t })
            ]);
        });
    }
};