REM Verify dbs...
npx sequelize-cli db:migrate:status

REM Create a migration skeleton
npx sequelize-cli migration:generate --name migration-new_data_cols

npx sequelize-cli db:migrate:status --env production

npx sequelize-cli db:migrate --env production