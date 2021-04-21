import { evaluationByCompetencyIdStudentId } from "./evaluation";

test("evaluationByCompetencyIdStudentId", () => {
  const evaluations = [
    { evaluation: { id: 2, competency_id: 3, student_id: 4 } },
    { evaluation: { id: 3, competency_id: 2, student_id: 6 } },
    { evaluation: { id: 1, competency_id: 3, student_id: 6 } },
  ];
  expect(evaluationByCompetencyIdStudentId(evaluations)).toStrictEqual({
    3: {
      4: { id: 2, competency_id: 3, student_id: 4 },
      6: { id: 1, competency_id: 3, student_id: 6 },
    },
    2: {
      6: { id: 3, competency_id: 2, student_id: 6 },
    },
  });
});
