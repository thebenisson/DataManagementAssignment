SELECT
  stations.Location,
  AVG(`PM2.5`) as `Mean particulate matter`,
  AVG(`VPM2.5`) as `Mean volatile particulate matter`
FROM records
  INNER JOIN stations ON stations.SiteID=records.SiteID
WHERE
  YEAR(records.`Date Time`)=2019
  AND CONVERT(records.`Date Time`, TIME) BETWEEN CONVERT("07:00:00", TIME) AND CONVERT("09:00:00", TIME)
GROUP BY records.SiteID;