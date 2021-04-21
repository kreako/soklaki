/// Group students by cycle
/// students is a an array like : [{ student_id: 1, cycle: "c3"},...]
/// Returns an object with cycle -> List<id> : {"c1": [1, 3], "c2": [2, 4]...}
export const groupStudentsByCycle = (students) => {
  if (students == null) {
    return {};
  }
  return students.reduce((acc, val) => {
    if (!(val.cycle in acc)) {
      acc[val.cycle] = [];
    }
    acc[val.cycle].push(val.student_id);
    return acc;
  }, {});
};

/// Build a student id to cycle mapping
/// students is a an array like : [{ student_id: 1, cycle: "c3"},...]
/// return something like : { id: cycle, ...}
export const studentsIdToCycle = (students) => {
  const mapping = {};
  for (const s of students) {
    mapping[s.student_id] = s.cycle;
  }
  return mapping;
};
