/// Group competencies by cycles
/// competencies is an array of id : [1, 2...]
/// Returns an object with cycle -> List<id> with all cycles inside (even empty ones)
export const groupCompetenciesByCycle = (store, competencies) => {
  const groups = {
    c1: [],
    c2: [],
    c3: [],
    c4: [],
  };
  for (const id of competencies) {
    const competency = store.getters.competencyById(id);
    if (competency.cycle == null) {
      // Could happen when the store is not yet full
      continue;
    }
    groups[competency.cycle].push(id);
  }
  return groups;
};

/// Return true if subjectId is in competency subjects list
export const isSubjectInCompetency = (subjectId, competency) => {
  const f = competency.subjects.find((x) => x.subject_id === subjectId);
  return f != undefined;
};
