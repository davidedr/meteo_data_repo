module.exports = {
    HOST: "localhost",
    PORT: 5433,
    USER: "postgres",
    PASSWORD: "postgres",
    DB: "meteo_data_repo",
    dialect: "postgres",
    logging: true,
    pool: { max: 5, min: 0, acquire: 30000, idle: 10000 }
}