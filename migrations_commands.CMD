REM Verify dbs...
npx sequelize-cli db:migrate:status

REM Create a migration skeleton
npx sequelize-cli migration:generate --name migration-new_data_cols

npx sequelize-cli db:migrate:status --env production --debug

npx sequelize-cli db:migrate --env production --debug

npx sequelize-cli db:migrate:undo --env production --debug

npx sequelize-cli db:migrate --env production --from 20201204094032-migration-rename-col_equilibrium_moisture_content_rel_equilibrium_moisture_content --debug 
