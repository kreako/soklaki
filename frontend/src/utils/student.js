import { estimateCycle } from "./cycle";

/// Return the cycle of the student at date (in string format)
/// Return the string "c1", "c2"...
export const studentCycleById = (store, date, studentId) => {
  const student = store.getters.studentById(studentId);
  if (student.birthdate == null) {
    // Best effort
    return null;
  }
  return estimateCycle(student.birthdate, date);
};

/// Group students by cycle at date
/// date is a string
/// students is a an array of id : [1, 2, 3...]
/// Returns an object with cycle -> List<id> : {"c1": [1, 3], "c2": [2, 4]...}
export const groupStudentsByCycle = (store, date, students) => {
  const cycles = {};
  for (const id of students) {
    const student = store.getters.studentById(id);
    if (student.birthdate === null) {
      // Ignore hopefully this is in the middle of store init
      continue;
    }
    const cycle = estimateCycle(student.birthdate, date);
    if (!(cycle in cycles)) {
      cycles[cycle] = [];
    }
    cycles[cycle].push(id);
  }
  return cycles;
};
