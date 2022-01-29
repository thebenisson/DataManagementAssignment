SELECT
  stations.SiteID AS `station number`,
  stations.Location AS `station name`,
  records.`Date Time`,
  MAX(records.CO) as `highest CO`
FROM
  records
  INNER JOIN stations ON stations.SiteID=records.SiteID;