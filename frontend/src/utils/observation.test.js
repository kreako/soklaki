import { isStudentObserved } from "./observation";

test("isStudentObserved", () => {
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
  expect(isStudentObserved(observation, 0)).toBeFalsy();
  expect(isStudentObserved(observation, 1)).toBeTruthy();
  expect(isStudentObserved(observation, 2)).toBeFalsy();
  expect(isStudentObserved(observation, 3)).toBeTruthy();
  expect(isStudentObserved(observation, 4)).toBeFalsy();
});
