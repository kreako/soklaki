/// Check if student id is already part of students of the observation
/// Used to filter out from selector the student that I already selected
export const isStudentObserved = (observation, studentId) => {
  for (const s of observation.students) {
    if (s.student_id === studentId) {
      return true;
    }
  }
  return false;
};
