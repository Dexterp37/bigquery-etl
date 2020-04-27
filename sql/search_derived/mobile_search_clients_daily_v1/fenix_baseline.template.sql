
-- baseline fields for {namespace}
SELECT
  DATE(submission_timestamp) AS submission_date,
  client_info.client_id,
  udf.mode_last(ARRAY_AGG(client_info.locale)) AS locale
FROM
  {namespace}.baseline
GROUP BY
  submission_date,
  client_id
