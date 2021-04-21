import { groupCompetenciesByCycle } from "./competency";

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
          return null;
        }
      },
    },
  };
  expect(groupCompetenciesByCycle(store, [1, 2, 4, 6, 5, 3])).toStrictEqual({
    c1: [1, 5],
    c2: [],
    c3: [2],
    c4: [4, 3],
  });
});
