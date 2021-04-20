/// Check if student id is already part of students of the observation
export const isStudentSelected = (observation, studentId) => {
  for (const s of observation.students) {
    if (s.student_id === studentId) {
      return true;
    }
  }
  return false;
};

/// For an observation, returns the list of non selected students
/// Taking in account the period of the observation (if any)
export const nonSelectedStudents = (store, observation) => {
  if (observation.period != null) {
    // There is an associated period
    const periodId = observation.period.id;
    const period = store.getters.periodById(periodId);
    return period.students
      .map((x) => x.student.id)
      .filter((id) => !isStudentSelected(observation, id));
  } else {
    // return the full set of students (even those not in school anymore)
    return store.state.sortedStudents.filter(
      (id) => !isStudentSelected(observation, id)
    );
  }
};
