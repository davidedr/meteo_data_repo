REM Folders creation
md meteo_data_repo
cd meteo_data_repo

REM 
pip install fake_useragent

npm --version
C:\"Program Files"\PostgreSQL\11\bin\postgres -V
C:\"Program Files"\PostgreSQL\11\bin\psql -V

REM Node Initializazion and libraries downloading
npm init
npm install --save express sequelize pg pg-hstore body-parser cors 

REN Client
npm install --save xmlhttprequest

REM
npm install --save sequelize-cli

REM Remove any previus instance
C:\"Program Files"\PostgreSQL\11\bin\dropdb.exe --echo --host=localhost --port=5433 --username=postgres meteo_data_repo

REM Database creation
C:\"Program Files"\PostgreSQL\11\bin\createdb.exe --echo --host=localhost --port=5433 --username=postgres meteo_data_repo
C:\"Program Files"\PostgreSQL\11\bin\createdb.exe --echo --host=localhost --port=5433 --username=postgres meteo_data_repo_development
C:\"Program Files"\PostgreSQL\11\bin\createdb.exe --echo --host=localhost --port=5433 --username=postgres meteo_data_repo_test

REM
REM Download and install PhantomJS
REM from https://bitbucket.org/ariya/phantomjs/downloads/
REM 

REM
REM Download and install Selenium
REM
pip install --save selenium

REM
REM Install logging library
REM
npm install --save winston