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
                queryInterface.addColumn('meteo_data', 'moon_phase_desc', { type: Sequelize.STRING, allowNull: true, defaultValue: null }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'sunrise_timestamp', { type: Sequelize.DATE, allowNull: true, defaultValue: null }, { transaction: t }),
                queryInterface.addColumn('meteo_data', 'sunset_timestamp', { type: Sequelize.DATE, allowNull: true, defaultValue: null }, { transaction: t }),
                queryInterface.addColumn('ws_capabilities', 'moon_phase_desc', { type: Sequelize.BOOLEAN, defaultValue: false }, { transaction: t }),
                queryInterface.addColumn('ws_capabilities', 'sunrise_timestamp', { type: Sequelize.BOOLEAN, defaultValue: false }, { transaction: t }),
                queryInterface.addColumn('ws_capabilities', 'sunset_timestamp', { type: Sequelize.BOOLEAN, defaultValue: false }, { transaction: t })
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
                queryInterface.removeColumn('meteo_data', 'moon_phase_desc', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'sunrise_timestamp', { transaction: t }),
                queryInterface.removeColumn('meteo_data', 'sunset_timestamp', { transaction: t }),
                queryInterface.removeColumn('ws_capabilities', 'moon_phase_desc', { transaction: t }),
                queryInterface.removeColumn('ws_capabilities', 'sunrise_timestamp', { transaction: t }),
                queryInterface.removeColumn('ws_capabilities', 'sunset_timestamp', { transaction: t })
            ]);
        });
    }
};