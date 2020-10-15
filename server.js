const express = require("express")
const bodyParser = require("body-parser")
const cors = require("cors")

const app = express()
var corsOptions = { origin: "http://localhost:8081" }
app.use(cors(corsOptions))

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))

const db = require("./app/models")
db.sequelize.sync({ force: true })
    .then(() => { console.log("DB dropped and re-created.") })
    .then(() => { console.log("Test data inserting...") })
    .then(() => { create_location() })

app.get("/", (req, res) => { res.json({ message: "Welcome!" }) })

require("./app/routes/meteo_data.routes")(app)
const PORT = process.env.PORT || 8080
app.listen(PORT, () => { console.log(`Server listening on port: ${PORT}`) })

//
//
//
function create_location() {
    const location = {
        name: 'Hotel "Marco Polo" Caorle',
        latitude: 45.5978224,
        longitude: 12.8839359,
        address_complete: "Via della Serenissima, 22, 30021 Caorle VE",
        street_1: "Via della Serenissima, 22",
        street_2: null,
        zip: "30021",
        town: "Caorle",
        province: "VE",
        country: "IT",
        note: "Meteo station @ https://www.hotelmarcopolocaorle.it/meteo/hmpolocaorle.php"
    }

    id = db.locations.create(location)
        .then(console.log("Location created."))
        .catch(err => console.log(`Error creating Location!`))

    id.sync.then(console.log(id))

}

function create_meteo_data() {

}