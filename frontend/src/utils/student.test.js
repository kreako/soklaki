import { groupStudentsByCycle, studentsIdToCycle } from "./student";

test("groupStudentsByCycle", () => {
  const students = [
    { student_id: 2, cycle: "c1" },
    { student_id: 3, cycle: "c2" },
    { student_id: 4, cycle: "c4" },
    { student_id: 5, cycle: "c3" },
    { student_id: 6, cycle: "c3" },
    { student_id: 7, cycle: "c1" },
  ];
  expect(groupStudentsByCycle(students)).toStrictEqual({
    c1: [2, 7],
    c2: [3],
    c3: [5, 6],
    c4: [4],
  });
  expect(groupStudentsByCycle(null)).toStrictEqual({});
});

test("studentsIdToCycle ", () => {
  const students = [
    { student_id: 2, cycle: "c1" },
    { student_id: 3, cycle: "c2" },
    { student_id: 5, cycle: "c3" },
    { student_id: 7, cycle: "c1" },
  ];
  expect(studentsIdToCycle(students)).toStrictEqual({
    2: "c1",
    3: "c2",
    5: "c3",
    7: "c1",
  });
});
