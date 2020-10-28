REM Verify dbs...
npx sequelize-cli db:migrate:status

REM Create a migration skeleton
npx sequelize-cli migration:generate --name migration-skeleton

npx sequelize-cli db:migrate:status --env production

npx sequelize-cli db:migrate --env production