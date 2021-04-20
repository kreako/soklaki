import { studentCycleById } from "./student";

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
