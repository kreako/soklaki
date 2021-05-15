import { isStudentSelected, nonSelectedStudents } from "./observation";

test("isStudentSelected", () => {
  const observation = {
    students: [
      {
        student_id: 1,
      },
      {
        student_id: 3,
      },
    ],
  };
  expect(isStudentSelected(observation, 0)).toBeFalsy();
  expect(isStudentSelected(observation, 1)).toBeTruthy();
  expect(isStudentSelected(observation, 2)).toBeFalsy();
  expect(isStudentSelected(observation, 3)).toBeTruthy();
  expect(isStudentSelected(observation, 4)).toBeFalsy();
});

test("nonSelectedStudents", () => {
  const store = {
    state: {
      sortedStudents: [0, 1, 3, 5, 7],
    },
    getters: {
      periodById: (id) => {
        return {
          students: [
            { student: { id: 1 } },
            { student: { id: 3 } },
            { student: { id: 5 } },
          ],
        };
      },
    },
  };
  const observation = {
    period: {
      eval_period_id: 1,
    },
    students: [
      {
        student_id: 3,
      },
    ],
  };
  expect(nonSelectedStudents(store, observation)).toStrictEqual([1, 5]);
  observation.period = null;
  expect(nonSelectedStudents(store, observation)).toStrictEqual([0, 1, 5, 7]);
});
