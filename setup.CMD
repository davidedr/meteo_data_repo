REM Folders creation
md meteo_data_repo
cd meteo_data_repo

REM Node Initializazion and libraries downloading
npm init
npm install express sequelize pg pg-hstore body-parser cors --save

REM Remove any previus instance
C:\"Program Files"\PostgreSQL\11\bin\dropdb.exe --echo --host=localhost --port=5433 --username=postgres meteo_data_repo

REM Database creation
C:\"Program Files"\PostgreSQL\11\bin\createdb.exe --echo --host=localhost --port=5433 --username=postgres meteo_data_repo