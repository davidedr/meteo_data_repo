'use strict';

const { QueryInterface } = require("sequelize/types");

module.exports = {
    up: async(queryInterface, Sequelize) => {
        return QueryInterface.sequelize.transaction(t => {
            return Promise.all([
                queryInterface.addColumn('locations', 'height_asl_m', {
                    type: Sequelize.DECIMAL,
                    defaultValue: null,
                    validate: { min: 0 }
                }, { transaction: t })
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
                queryInterface.removeColumn('locations', 'height_asl_m', { transaction: t })
            ]);
        });
    }
};