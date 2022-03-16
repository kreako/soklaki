CREATE
OR REPLACE VIEW "public"."summary_report_period" AS
SELECT
  eval_period.id AS eval_period_id,
  summary_report.id AS summary_report_id
FROM
  (
    (
      eval_period
      JOIN student ON ((eval_period.group_id = student.group_id))
    )
    JOIN summary_report ON (
      (
        (summary_report.student_id = student.id)
        AND (summary_report.date >= eval_period.start)
        AND (summary_report.date <= eval_period."end")
      )
    )
  );
