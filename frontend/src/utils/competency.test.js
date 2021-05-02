import { groupCompetenciesByCycle, isSubjectInCompetency } from "./competency";

test("groupCompetenciesByCycle", () => {
  const store = {
    getters: {
      competencyById: (id) => {
        if (id === 1) {
          return { cycle: "c1" };
        } else if (id === 2) {
          return { cycle: "c3" };
        } else if (id === 3) {
          return { cycle: "c4" };
        } else if (id === 4) {
          return { cycle: "c4" };
        } else if (id === 5) {
          return { cycle: "c1" };
        } else {
          return { cycle: null };
        }
      },
    },
  };
  expect(
    groupCompetenciesByCycle(store, [1, 2, 4, 6, null, 5, 3])
  ).toStrictEqual({
    c1: [1, 5],
    c2: [],
    c3: [2],
    c4: [4, 3],
  });
});

test("isSubjectInCompetency", () => {
  const competency = {
    subjects: [
      { id: 232, subject_id: 2 },
      { id: 231, subject_id: 4 },
    ],
  };
  expect(isSubjectInCompetency(2, competency)).toBeTruthy();
  expect(isSubjectInCompetency(3, competency)).toBeFalsy();
});
