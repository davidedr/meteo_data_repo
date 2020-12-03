from scanner_meteosystem_alike_ws import scan_meteosystem_alike
from scanner_meteovenezia_alike_ws import scan_meteovenezia_alike
from scanner_hotelmarcopolo_caorle_alike_ws import scan_hotelmarcopolo_caorle_alike
from scanner_meteonetwork_vnt336_alike_ws import scan_meteonetwork_vnt336_alike
from scanner_meteonetwork_vnt432_alike_ws import scan_meteonetwork_vnt432_alike
from scanner_cellarda_sud_alike_ws import scan_cellarda_sud_ws_alike
from scanner_cellarda_nord_alike_ws import scan_cellarda_nord_ws_alike
from scanner_stazione_amatoriale_feltre_alike import scan_stazione_amatoriale_feltre_alike
from scanner_feltre_meteo_alike import scan_feltre_meteo_alike
from scanner_osservatorio_metereologico_festisei_alike import scan_osservatorio_metereologico_festisei_alike

#
#
#
locations_json=[None]*40

locations_json[1]={
    "name": 'Hotel "Marco Polo", Caorle',
    "latitude": 45.5978224,
    "longitude": 12.8839359,
    "address_complete": "Via della Serenissima, 22, 30021 Caorle VE",
    "street_1": "Via della Serenissima, 22",
    "street_2": None,
    "zip": "30021",
    "town": "Caorle",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station https://www.hotelmarcopolocaorle.it/meteo/hmpolocaorle.php",
    "height_asl_m": 0
}

locations_json[4]={
    "name": 'Bagno Margherita Caorle',
    "latitude": 45.588340,
    "longitude": 12.861544,
    "address_complete": "Viale Lepanto, 13A, 30021 Porto Santa Margherita VE",
    "street_1": "Viale Lepanto, 13A",
    "street_2": "Porto Santa Margherita",
    "zip": "30021",
    "town": "Caorle",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station https://www.meteo-caorle.it/, Porto Santa Margherita, Spiaggia Est, Caorle, Venezia",
    "height_asl_m": 0
}

locations_json[8]={
    "name": 'San Giorgio, Venezia',
    "latitude": 45.429939,
    "longitude": 12.342716,
    "address_complete": "30100 Venezia, Città Metropolitana di Venezia",
    "street_1": "",
    "street_2": "",
    "zip": "30100",
    "town": "Venezia",
    "province": "Città Metropolitana di Venezia",
    "country": "IT",
    "note": "Meteo station https://www.meteo-venezia.net/compagnia01.php, Isola di San Giorgio Maggiore, Venezia",
    "height_asl_m": 0
}

locations_json[9]={
    "name": 'Punta San Giuliano, Mestre-Venezia',
    "latitude": 45.629892,
    "longitude": 12.997956,
    "address_complete": "Via S. Giuliano, 23, 30174 Venezia VE",
    "street_1": "Via S. Giuliano, 23",
    "street_2": "",
    "zip": "30174",
    "town": "Mestre",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station https://www.meteo-venezia.net/, Punta San Giuliano, Mestre-Venezia",
    "height_asl_m": 0
}

locations_json[10]={
    "name": 'Laguna Park Hotel, Bibione, Venezia',
    "latitude": 45.466542,
    "longitude": 12.282729,
    "address_complete": "Via Passeggiata al Mare, 20, 30028 Bibione VE",
    "street_1": "Via Passeggiata al Mare, 20",
    "street_2": "",
    "zip": "30028",
    "town": "Bibione",
    "province": "VE",
    "country": "IT",
    "note": "Meteo station https://www.bibione-meteo.it/, Bibione, Venezia",
    "height_asl_m": 0
}

locations_json[11]={
    "name": 'Meteo Network stazione meteo di Feltre',
    "latitude": 46.016,
    "longitude": 11.895,
    "address_complete": None,
    "street_1": None,
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Meteo station http://my.meteonetwork.it/station/vnt336/, Model: MTX, Type: Semi-Urbana, Ubicazione: Campo aperto",
    "height_asl_m": 267
}

locations_json[12]={
    "name": 'Osservatorio meteorologico di I.I.S. Agrario “Antonio della Lucia” di Feltre (BL)',
    "latitude": 46.036,
    "longitude": 11.937,
    "address_complete": "Via Vellai, 41, 32032 Vellai BL",
    "street_1": "Via Vellai,",
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Meteo station, http://www.meteosystem.com/dati/feltre/dati.php, Model: Davis Vantage Pro 2",
    "height_asl_m": 330
}

locations_json[15]={
    "name": 'LaCrosse WS2300 di Pellencin Giorgio, Cellarda Sud, Feltre (BL)',
    "latitude": 46.011,
    "longitude": 11.966,
    "address_complete": "Fraz. Cellarda, Sud, 32032 Feltre (BL)",
    "street_1": "Fraz. Cellarda",
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Stazione Meteo di Pellencin Giorgio, Cellarda Sud, http://www.celarda.altervista.org/index.htm, Model: LaCrosse WS2300",
    "height_asl_m": 225
}

locations_json[16]={
    "name": 'LaCrosse WS2300 di Pellencin Giorgio, Cellarda Nord, Feltre (BL)',
    "latitude": 46.011,
    "longitude": 11.966,
    "address_complete": "Fraz. Cellarda, Nord, 32032 Feltre (BL)",
    "street_1": "Fraz. Cellarda",
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Stazione Meteo di Pellencin Giorgio, Cellarda Nord, http://www.meteocelarda.altervista.org/index.htm, Model: LaCrosse WS2300",
    "height_asl_m": 225
}

locations_json[17]={
    "name": 'Stazione meteo di Viale Fusinato, Feltre',
    "latitude": 46.04333,
    "longitude": 11.91222,
    "address_complete": "Viale Fusinato, 32032 Feltre (BL)",
    "street_1": "Viale Fusinato",
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Stazione meteo di Viale Fusinato, Feltre, http://my.meteonetwork.it/station/vnt432/stazione, Model: Davis Vantage pro 2 plus wireless",
    "height_asl_m": 320
}

locations_json[18]={
    "name": 'Stazione meteo amatoriale di Feltre',
    "latitude": None,
    "longitude": None,
    "address_complete": None,
    "street_1": None,
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Stazione meteo amatoriale di Feltre, http://stazioni2.soluzionimeteo.it/feltre/indexDesktop.php, Model: Ventus w835",
    "height_asl_m": 250
}

locations_json[19]={
    "name": 'Feltre meteo',
    "latitude": 46.06472,
    "longitude": 11.90472,
    "address_complete": None,
    "street_1": None,
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Stazione meteo amatoriale di Feltre, http://www.feltremeteo.it/weather/index.php, Model: Oregon Scientific WMR180 + UV",
    "height_asl_m": 240
}

locations_json[20]={
    "name": 'Stazione meteo amatoriale di Mugnai',
    "latitude": None,
    "longitude": None,
    "address_complete": None,
    "street_1": None,
    "street_2": None,
    "zip": "32032",
    "town": "Feltre",
    "province": "BL",
    "country": "IT",
    "note": "Stazione meteo amatoriale di Feltre, http://www.meteomugnai.it/indexDesktop.php, Model: Ventus w835",
    "height_asl_m": 250
}

locations_json[21]={
    "name": 'Osservatorio Meteorologico di Festisei, Pedavena',
    "latitude": 46.042,
    "longitude": 11.869,
    "address_complete": "Via Festisei, 32034 Pedavena (BL)",
    "street_1": "Via Festisei",
    "street_2": None,
    "zip": "32034",
    "town": "Pedavena",
    "province": "BL",
    "country": "IT",
    "note": "Osservatorio Meteorologico di Festisei, Pedavena, http://festisei.meteolodi.net/cam1/meteo/, Model: Davis Vantage Pro 2",
    "height_asl_m": 465
}

ws_capabilities=[None]*40
ws_capabilities[20]={
    "location_id": 20,
    "timestamp_ws": True,
    "wind_speed_knots": True,
    "wind_direction_deg": True,
    "barometric_pressure_ssl_hPa": True,
    "rain_today_mm": True,
    "rain_rate_mmh": True,
    "temperature_cels": True,
    "rel_humidity": True,
    "heat_index_cels": True,
    "wind_gust_knots": True,
    "dew_point_cels": True,
    "wind_chill_cels": True,
    "ground_temperature_cels": True,
    "solar_irradiance_wpsm": True,
    "rel_leaf_wetness": True,
    "soil_moisture_cb": True,
    "rain_this_month_mm": True,
    "rain_this_year_mm": True,
    "evapotranspiration_today_mm": True,
    "evapotranspiration_this_month_mm": True,
    "evapotranspiration_this_year_mm": True,
    "perceived_temperature_cels": True,
    "average_wind_speed_knots": True,
    "rain_in_last_storm_event_mm": True
}

ws_capabilities[21]={
    "location_id": 20,
    "timestamp_ws": True,
    "temperature_cels": True,
    "perceived_temperature_cels": True,
    "humidex_cels": True,
    "rel_humidity": True,
    "absolute_humidity_gm3": True,
    "saturated_vapor_pressure_hPa": True,
    "barometric_pressure_ssl_hPa": True,
    "barometric_pressure_wsl_hPa": True,
    "wind_speed_knots": True,
    "wind_direction_deg": True,
    "wind_gust_knots": True,
    "windrun_km": True,
    "rain_rate_mmh": True,
    "rain_today_mm": True,
    "rain_this_month_mm": True,
    "rain_this_year_mm": True,
    "dew_point_cels": True,
    "wind_chill_cels": True,
    "wet_bulb_temperature_cels": True,
    "uv_index": True,
    "heat_index_cels": True
}

# "scan_time_interval" in seconds
servers = [
  { "location_id":  1, "location": locations_json[ 1], "to_be_started": True, "name": "hotelmarcopolo_caorle", "url": "https://www.hotelmarcopolocaorle.it/meteo/hmpolocaorle.php", "scanner": scan_hotelmarcopolo_caorle_alike, "scan_time_interval": 55 }, # Wait for 50 secs
  { "location_id":  4, "location": locations_json[ 4], "to_be_started": True, "name": "bagnomargherita_caorle", "url": "https://www.meteo-caorle.it/", "scanner": scan_meteovenezia_alike, "scan_time_interval": 55 },
  { "location_id":  8, "location": locations_json[ 8], "to_be_started": True, "name": "sangiorgio_venezia", "url": "https://www.meteo-venezia.net/compagnia01.php", "scanner": scan_meteovenezia_alike, "scan_time_interval": 55 },
  { "location_id":  9, "location": locations_json[ 9], "to_be_started": True, "name": "puntasangiuliano_mestre", "url": "https://www.meteo-venezia.net/", "scanner": scan_meteovenezia_alike, "scan_time_interval": 55 },
  { "location_id": 10, "location": locations_json[10], "to_be_started": True, "name": "lagunaparkhotel_bibione", "url": "https://www.bibione-meteo.it/", "scanner": scan_meteovenezia_alike, "scan_time_interval":55 },
  { "location_id": 11, "location": locations_json[11], "to_be_started": True, "name": "meteonetwork_feltre", "url": "http://my.meteonetwork.it/station/vnt336/", "scanner": scan_meteonetwork_vnt336_alike, "scan_time_interval": 60*30 }, # Wait for half an hour
  { "location_id": 12, "location": locations_json[12], "to_be_started": True, "name": "agrario_feltre", "url": "http://www.meteosystem.com/dati/feltre/dati.php", "scanner": scan_meteosystem_alike, "scan_time_interval": 55 },
  { "location_id": 15, "location": locations_json[15], "to_be_started": True, "name": "cellarda_sud_feltre", "url": {"1": "http://www.celarda.altervista.org/index.htm", "2": "http://my.meteonetwork.it/station/vnt374/" }, "scanner": scan_cellarda_sud_ws_alike, "scan_time_interval": 60*5 },
  { "location_id": 16, "location": locations_json[16], "to_be_started": True, "name": "cellarda_nord_feltre", "url": "http://www.meteocelarda.altervista.org/index.htm", "scanner": scan_cellarda_nord_ws_alike, "scan_time_interval": 60*5 }, # Wait five minutes
  { "location_id": 17, "location": locations_json[17], "to_be_started": True, "name": "meteonetwork_vialefusinato_feltre", "url": "http://my.meteonetwork.it/station/vnt432/", "scanner": scan_meteonetwork_vnt432_alike, "scan_time_interval": 60*3 }, # Wait for half an hour  
  { "location_id": 18, "location": locations_json[18], "to_be_started": True, "name": "stazione_amatoriale_feltre", "url": "http://stazioni2.soluzionimeteo.it/feltre/indexDesktop.php", "scanner": scan_stazione_amatoriale_feltre_alike, "scan_time_interval": 100 },
  { "location_id": 19, "location": locations_json[19], "to_be_started": True, "name": "feltre_meteo", "url": "http://www.feltremeteo.it/weather/index.php", "scanner": scan_feltre_meteo_alike, "scan_time_interval": 55*5 },
  { "location_id": 20, "location": locations_json[20], "to_be_started": True, "name": "stazione_amatoriale_mugnai", "url": "http://www.meteomugnai.it/indexDesktop.php", "scanner": scan_stazione_amatoriale_feltre_alike, "scan_time_interval": 100, "ws_capabilities": ws_capabilities[20] },
  { "location_id": 21, "location": locations_json[21], "to_be_started": False, "name": "osservatorio_metereologico_festisei", "url": "http://festisei.meteolodi.net/cam1/meteo/", "scanner": scan_osservatorio_metereologico_festisei_alike, "scan_time_interval": 100, "ws_capabilities": ws_capabilities[21] }
]

SCAN_TIME_INTERVAL_DEFAULT=50 # Sec
