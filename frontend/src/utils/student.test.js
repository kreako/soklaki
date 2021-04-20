import { studentCycleById, groupStudentsByCycle } from "./student";

test("studentCycleById", () => {
  const store = {
    getters: {
      studentById: (id) => {
        if (id === 1) {
          return { birthdate: "2015-11-02" };
        } else {
          return { birthdate: null };
        }
      },
    },
  };
  expect(studentCycleById(store, "2021-10-01", 1)).toBe("c2");
  expect(studentCycleById(store, "2021-10-01", 2)).toBeNull();
});

test("groupStudentsByCycle", () => {
  const store = {
    getters: {
      studentById: (id) => {
        if (id === 1) {
          return { birthdate: "2010-11-02" };
        } else if (id === 2) {
          return { birthdate: "2013-11-02" };
        } else if (id === 3) {
          return { birthdate: "2014-02-02" };
        } else if (id === 4) {
          return { birthdate: "2015-11-02" };
        } else if (id === 5) {
          return { birthdate: "2016-01-02" };
        } else {
          return { birthdate: null };
        }
      },
    },
  };
  expect(
    groupStudentsByCycle(store, "2020-10-01", [1, 2, 6, 5, 3, 4])
  ).toStrictEqual({ c1: [5, 4], c2: [2, 3], c3: [1] });
});
