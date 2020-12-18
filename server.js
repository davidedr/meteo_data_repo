const winston = require('winston')
const format = winston.format
const console_transport = new winston.transports.Console()
const error_logs_file_transport = new winston.transports.File({ filename: 'log/meteo_data_repo_server_error.log', level: 'error' })
const all_logs_file_transport = new winston.transports.File({ filename: 'log/meteo_data_repo_server_all_logs.log', level: 'info' })

const winston_options = {
    format: format.combine(format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }), format.label({ label: "meteo_data_repo_logger" }), format.prettyPrint()),
    transports: [console_transport, error_logs_file_transport, all_logs_file_transport]
}

const logger = new winston.createLogger(winston_options)

logger.info('Logger initilized!')

const express = require("express")
const bodyParser = require("body-parser")
const cors = require("cors")

const app = express()
var corsOptions = { origin: "http://localhost:8081" }
app.use(cors(corsOptions))

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))

logger.info('Init db...')
const db = require("./app/models")
db.sequelize.sync({ force: false })
    .then(() => { logger.log('Db initializated.') })

logger.info('Setting up default route...')
app.get("/", (req, res) => { res.json({ message: "Welcome!" }) })

require("./app/routes/meteo_data.routes")(app)
require("./app/routes/location.routes")(app)
require("./app/routes/ws_capabilities.routes")(app)
const PORT = process.env.PORT || 8080
app.listen(PORT, () => { logger.info(`Server listening on port: ${PORT}`) })
logger.info('Server setup finished.')