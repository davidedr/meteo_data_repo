ALTER TABLE meteo_data ADD COLUMN wind_gust_knots NUMERIC DEFAULT NULL
ALTER TABLE meteo_data ADD COLUMN dew_point_cels NUMERIC DEFAULT NULL
ALTER TABLE "meteo_data" ALTER COLUMN  "rain_today_mm" TYPE NUMERIC
UPDATE locations SET height_asl_m=330 WHERE id=12;
UPDATE locations SET height_asl_m=267 WHERE id=11;
SELECT * FROM locations;


ALTER TABLE ws_capabilities
RENAME COLUMN equilibrium_moisture_content TO rel_equilibrium_moisture_content;

-- GET LAST OBSERVATION'S TIMESTAMP FOR EACH STATION
SELECT DISTINCT ON (LOCATION_ID) LOCATION_ID, ID, TIMESTAMP_WS FROM METEO_DATA ORDER BY LOCATION_ID, TIMESTAMP_WS DESC;

-- GET TOTAL NUMBER OF OBSERVATIONS
SELECT COUNT(*) FROM METEO_DATA;

-- GET NUMBER OF OBSERVATIONS FOR EACH STATION
SELECT LOCATIONS.ID, LOCATIONS.NAME, LOCATIONS.TOWN, COUNT(*) FROM meteo_data, LOCATIONS WHERE METEO_DATA.LOCATION_ID=LOCATIONS.ID GROUP BY LOCATIONS.ID ORDER BY LOCATIONS.ID;

-- GET NUMBER OF OBSERVATIONS FOR EACH TOWN
SELECT LOCATIONS.TOWN, COUNT(*) FROM meteo_data, LOCATIONS WHERE METEO_DATA.LOCATION_ID=LOCATIONS.ID GROUP BY LOCATIONS.TOWN ORDER BY LOCATIONS.TOWN;

--- TODAY'S MIN, MAX TEMPERATURES FOR EACH LOCATION
SELECT LOCATION_ID, DATE(timestamp_ws), MIN(TEMPERATURE_CELS), MAX(TEMPERATURE_CELS) FROM METEO_DATA WHERE DATE(timestamp_ws)=DATE(NOW()) GROUP BY LOCATION_ID, DATE(timestamp_ws);

--- TODAY'S MIN, MAX TEMPERATURES FOR EACH LOCATION, 2 - JOIN WITH LOCATIONS' DATA
SELECT LOCATION_ID, LOCATIONS.NAME, LOCATIONS.TOWN, DATE(timestamp_ws), MIN(TEMPERATURE_CELS), MAX(TEMPERATURE_CELS)
	FROM METEO_DATA, LOCATIONS 
	WHERE METEO_DATA.LOCATION_ID=LOCATIONS.ID AND DATE(timestamp_ws)=DATE(NOW()) GROUP BY LOCATION_ID, LOCATIONS.TOWN, LOCATIONS.NAME, DATE(timestamp_ws);

--- WRONG wind_force_beaufort_desc COLUMN CONTENT DISCOVERY
SELECT wind_force_beaufort_desc, COUNT(*) FROM METEO_DATA WHERE wind_force_beaufort_desc IN ('N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'WNW', 'NW', 'NNW') GROUP BY wind_force_beaufort_desc;

SELECT id, location_id, timestamp_ws, wind_force_beaufort_desc FROM METEO_DATA WHERE wind_force_beaufort_desc='W' ORDER BY ID DESC;

SELECT * FROM METEO_DATA WHERE LOCATION_ID>=26 ORDER BY ID DESC;

SELECT id, location_id, timestamp_ws, wind_force_beaufort_desc from METEO_DATA WHERE LOCATION_ID>=26 ORDER BY ID DESC;

--- LAST RECORD BY LOCATION_ID
SELECT max(id) FROM meteo_data GROUP BY location_id;

--- LAST RECORDED TEMPERATURE (AND SO "CURRENT", HOPEFULLY) BY LOCATION
select id, location_id, meteo_data.timestamp_ws, temperature_cels
	from meteo_data where id IN (SELECT max(id) FROM meteo_data GROUP BY location_id)
	ORDER BY location_id;

--- LAST RECORDED TEMPERATURE (AND SO "CURRENT TEMPERATURE", HOPEFULLY) BY LOCATION - VERSION WITH LOCATIONS' DATA
select meteo_data.id, meteo_data.timestamp_ws, meteo_data.location_id, locations.name, locations.town, meteo_data.temperature_cels
	from meteo_data, locations where meteo_data.location_id=locations.id and meteo_data.id IN (SELECT max(id) FROM meteo_data GROUP BY location_id)
	ORDER BY location_id;

--- AVERAGES BY TOWN USING THE MOST RECENT DATA (IN TERMS OF ID FOR EACH LOCATION)
SELECT locations.town, AVG(meteo_data.temperature_cels)
	from meteo_data, locations where meteo_data.location_id=locations.id and meteo_data.id IN (SELECT max(id) FROM meteo_data GROUP BY location_id) 
	GROUP BY locations.town
	ORDER BY locations.town;

--- AVERAGES AND STDDEVs BY TOWN, ROUNDED USING THE MOST RECENT DATA (IN TERMS OF ID FOR EACH LOCATION)
SELECT locations.town, ROUND(AVG(meteo_data.temperature_cels), 1) AS avg_temperature_cels, ROUND(STDDEV_SAMP(meteo_data.temperature_cels), 1) AS stddev_temperature_cels, round(AVG(meteo_data.rel_humidity), 2) AS avg_rel_humidity, ROUND(AVG(meteo_data.wind_speed_knots), 2) AS avg_wind_speed_knots
	from meteo_data, locations where meteo_data.location_id=locations.id and meteo_data.id IN (SELECT max(id) FROM meteo_data GROUP BY location_id) 
	GROUP BY locations.town
	ORDER BY locations.town;

--- AVERAGES,  STDDEVs, NUM SAMPLES BY TOWN, ROUNDED USING THE MOST RECENT DATA (IN TERMS OF ID FOR EACH LOCATION)
SELECT locations.town, ROUND(AVG(meteo_data.temperature_cels), 1) AS avg_temperature_cels, ROUND(STDDEV_SAMP(meteo_data.temperature_cels), 1) AS stddev_temperature_cels, count(meteo_data.temperature_cels) AS num_samples_temperature_cels,
	round(AVG(meteo_data.rel_humidity), 2) AS avg_rel_humidity, ROUND(STDDEV_SAMP(meteo_data.rel_humidity), 1) AS stddev_rel_humidity, count(meteo_data.rel_humidity) AS num_samples_rel_humidity,
	ROUND(AVG(meteo_data.wind_speed_knots), 2) AS avg_wind_speed_knots, ROUND(STDDEV_SAMP(meteo_data.wind_speed_knots), 1) AS stddev_wind_speed_knots, count(meteo_data.wind_speed_knots) AS num_samples_wind_speed_knots
	from meteo_data, locations where meteo_data.location_id=locations.id and meteo_data.id IN (SELECT max(id) FROM meteo_data GROUP BY location_id) 
	GROUP BY locations.town
	ORDER BY locations.town;

--- AVERAGES,  STDDEVs, NUM SAMPLES BY TOWN, ROUNDED, USING TODAY'S DATA ONLY
SELECT locations.town, ROUND(AVG(meteo_data.temperature_cels), 1) AS avg_temperature_cels, ROUND(STDDEV_SAMP(meteo_data.temperature_cels), 1) AS stddev_temperature_cels, count(meteo_data.temperature_cels) AS num_samples_temperature_cels,
	ROUND(AVG(meteo_data.rel_humidity), 2) AS avg_rel_humidity, ROUND(STDDEV_SAMP(meteo_data.rel_humidity), 1) AS stddev_rel_humidity, count(meteo_data.rel_humidity) AS num_samples_rel_humidity,
	ROUND(AVG(meteo_data.wind_speed_knots), 2) AS avg_wind_speed_knots, ROUND(STDDEV_SAMP(meteo_data.wind_speed_knots), 1) AS stddev_wind_speed_knots, count(meteo_data.wind_speed_knots) AS num_samples_wind_speed_knots
	from meteo_data, locations where meteo_data.location_id=locations.id and meteo_data.id IN (SELECT max(id) FROM meteo_data WHERE DATE(METEO_DATA.TIMESTAMP_WS)=DATE(NOW()) GROUP BY location_id) 
	GROUP BY locations.town
	ORDER BY locations.town;

--- MOST RECENT DATA ROW FROM ANY LOCATIONS USING TODAY'S DATA ONLY
--- USEFUL BECAUSE SOME WSs MIGHT BE LAGGING BEHIND
SELECT location_id, max(id) FROM meteo_data WHERE DATE(METEO_DATA.TIMESTAMP_WS)=DATE(NOW()) GROUP BY location_id;

--- select data point no older than 30 min (60 sec * 30 min = 1800 sec)
SELECT DATE_PART('epoch', meteo_data."createdAt"-NOW()) AS delta_epoch, *
	FROM METEO_DATA
	WHERE abs(DATE_PART('epoch', meteo_data."createdAt"-NOW()))<=1800
	ORDER BY meteo_data."createdAt" DESC;

--- observations in the last 24 hours (60 sec * 30 min * 24 hour = 86400 sec)
SELECT DATE_PART('epoch', meteo_data."timestamp_ws"-NOW()) AS delta_epoch, *
	FROM METEO_DATA
	WHERE abs(DATE_PART('epoch', meteo_data."createdAt"-NOW()))<=86400
	ORDER BY location_id ASC, id ASC;


SELECT locations.town, ROUND(AVG(meteo_data.temperature_cels), 1) AS avg_temperature_cels, ROUND(STDDEV_SAMP(meteo_data.temperature_cels), 1) AS stddev_temperature_cels, count(meteo_data.temperature_cels) AS num_samples_temperature_cels,
	ROUND(AVG(meteo_data.rel_humidity), 2) AS avg_rel_humidity, ROUND(STDDEV_SAMP(meteo_data.rel_humidity), 1) AS stddev_rel_humidity, count(meteo_data.rel_humidity) AS num_samples_rel_humidity,
	ROUND(AVG(meteo_data.wind_speed_knots), 2) AS avg_wind_speed_knots, ROUND(STDDEV_SAMP(meteo_data.wind_speed_knots), 1) AS stddev_wind_speed_knots, count(meteo_data.wind_speed_knots) AS num_samples_wind_speed_knots
	from meteo_data, locations where meteo_data.location_id=locations.id and meteo_data.id IN (SELECT max(id) FROM meteo_data WHERE DATE(METEO_DATA.TIMESTAMP_WS)=DATE(NOW()) GROUP BY location_id) 
	GROUP BY locations.town
	ORDER BY locations.town;

select meteo_data.id, meteo_data.timestamp_ws, meteo_data.location_id, locations.name, locations.town, meteo_data.temperature_cels, round(meteo_data.wind_speed_knots, 2) AS wind_speed_knots
	from meteo_data, locations where meteo_data.location_id=locations.id and meteo_data.id IN (SELECT max(id) FROM meteo_data GROUP BY location_id)
	ORDER BY location_id;
	
SELECT LOCATION_ID, LOCATIONS.NAME, LOCATIONS.TOWN, DATE(timestamp_ws), MIN(TEMPERATURE_CELS), MAX(TEMPERATURE_CELS), MAX(TEMPERATURE_CELS)-MIN(TEMPERATURE_CELS) AS EXCURSION
	FROM METEO_DATA, LOCATIONS 
	WHERE METEO_DATA.LOCATION_ID=LOCATIONS.ID AND DATE(timestamp_ws)=DATE(NOW()) GROUP BY LOCATION_ID, LOCATIONS.TOWN, LOCATIONS.NAME, DATE(timestamp_ws);
	
SELECT * FROM METEO_DATA WHERE LOCATION_ID=12 ORDER BY timestamp_ws DESC;
