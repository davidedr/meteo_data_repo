ALTER TABLE meteo_data ADD COLUMN wind_gust_knots NUMERIC DEFAULT NULL
ALTER TABLE meteo_data ADD COLUMN dew_point_cels NUMERIC DEFAULT NULL
ALTER TABLE "meteo_data" ALTER COLUMN  "rain_today_mm" TYPE NUMERIC
UPDATE locations SET height_asl_m=330 WHERE id=12;
UPDATE locations SET height_asl_m=267 WHERE id=11;
SELECT * FROM locations;

