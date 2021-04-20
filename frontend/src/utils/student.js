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
