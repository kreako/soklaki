/// Build a competency id -> student id -> evaluation cache
/// evaluations is a list of evaluation object : [{competency_id: 8, student_id: 42}]
export const evaluationByCompetencyIdStudentId = (evaluations) => {
  const mapping = {};
  for (const e of evaluations) {
    const evaluation = e.evaluation;
    if (!(evaluation.competency_id in mapping)) {
      mapping[evaluation.competency_id] = {};
    }
    mapping[evaluation.competency_id][evaluation.student_id] = evaluation;
  }
  return mapping;
};
