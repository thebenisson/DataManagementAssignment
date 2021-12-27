SELECT
  stations.SiteID,
  stations.Location,
  CONCAT(geopoints.Latitude, ', ', geopoints.Longitude) as geo_point_2d,
  records.`Date Time`,
  records.NOx,
  records.NO2,
  records.NO,
  records.PM10,
  records.VPM10,
  records.NVPM10,
  records.`PM2.5`,
  records.`VPM2.5`,
  records.`NVPM2.5`,
  records.CO,
  records.O3,
  records.SO2,
  records.Temperature,
  records.RH,
  records.`Air Pressure`,
  records.DateStart,
  records.DateEnd,
  records.Current,
  records.`Instrument Type`
FROM
  stations
  INNER JOIN geopoints ON geopoints.SiteID=stations.SiteID
  INNER JOIN records ON records.SiteID = stations.SiteID
WHERE
  stations.SiteID=500 AND  `records`.`date time` >= CAST('2019' AS DATE);