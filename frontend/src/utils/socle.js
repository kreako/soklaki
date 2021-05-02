import { isSubjectInCompetency } from "./competency";

const parentRanks = (state, containerId) => {
  if (containerId == null) {
    // Init case
    return [];
  }
  // General recursion
  const container = state.containers[containerId];
  return [...parentRanks(state, container.container_id), container.rank];
};

export const computeRanks = ({ state, rank, containerId }) => {
  const parents = parentRanks(state, containerId);
  parents.push(rank);
  const fullRank = parents.join(".") + ".";
  const alphaFullRank =
    parents.map((x) => x.toString().padStart(4, "0")).join(".") + ".";
  return { alphaFullRank, fullRank };
};

const filterCompetenciesBySubject = (competencies, subjectId) =>
  competencies.filter((c) => isSubjectInCompetency(subjectId, c));

const filterContainer2BySubject = (children, subjectId) => {
  const filtered = [];
  for (const container of children) {
    const competencies = filterCompetenciesBySubject(
      container.competencies,
      subjectId
    );
    if (competencies.length > 0) {
      filtered.push({
        id: container.id,
        competencies: competencies,
      });
    }
  }
  return filtered;
};

export const filterSocleBySubject = (socle, subjectId) => {
  // assume that in container level 1 children and competencies are mutually exclusive
  const filtered = [];
  for (const container1 of socle) {
    const competencies = filterCompetenciesBySubject(
      container1.competencies,
      subjectId
    );
    if (competencies.length > 0) {
      filtered.push({
        id: container1.id,
        children: [],
        competencies: competencies,
      });
      continue;
    }
    const children = filterContainer2BySubject(container1.children, subjectId);
    if (children.length > 0) {
      filtered.push({
        id: container1.id,
        children: children,
        competencies: [],
      });
      continue;
    }
  }
  return filtered;
};

export const filterSocleBy2Ranks = (state, socle, rank1, rank2) => {
  for (const container1 of socle) {
    if (state.socle.containers[container1.id].rank != rank1) {
      continue;
    }
    for (const competency of container1.competencies) {
      if (state.socle.competencies[competency.id].rank == rank2) {
        return [
          {
            id: container1.id,
            children: [],
            competencies: [competency],
          },
        ];
      }
    }
  }
  return [];
};

export const filterSocleBy3Ranks = (state, socle, rank1, rank2, rank3) => {
  for (const container1 of socle) {
    if (state.socle.containers[container1.id].rank != rank1) {
      continue;
    }
    for (const container2 of container1.children) {
      if (state.socle.containers[container2.id].rank != rank2) {
        continue;
      }
      for (const competency of container2.competencies) {
        if (state.socle.competencies[competency.id].rank == rank3) {
          return [
            {
              id: container1.id,
              children: [
                {
                  id: container2.id,
                  competencies: [competency],
                },
              ],
              competencies: [],
            },
          ];
        }
      }
    }
  }
  return [];
};

const isRegexCompetency = (state, competency, regex) =>
  regex.test(state.socle.competencies[competency.id].text);

const filterCompetenciesByRegex = (state, competencies, regex) =>
  competencies.filter((c) => isRegexCompetency(state, c, regex));

const filterContainer2ByRegex = (state, children, regex) => {
  const filtered = [];
  for (const container of children) {
    const competencies = filterCompetenciesByRegex(
      state,
      container.competencies,
      regex
    );
    if (competencies.length > 0) {
      filtered.push({
        id: container.id,
        competencies: competencies,
      });
    }
  }
  return filtered;
};

export const filterSocleByRegex = (state, socle, regex) => {
  // assume that in container level 1 children and competencies are mutually exclusive
  const filtered = [];
  for (const container1 of socle) {
    const competencies = filterCompetenciesByRegex(
      state,
      container1.competencies,
      regex
    );
    if (competencies.length > 0) {
      filtered.push({
        id: container1.id,
        children: [],
        competencies: competencies,
      });
      continue;
    }
    const children = filterContainer2ByRegex(state, container1.children, regex);
    if (children.length > 0) {
      filtered.push({
        id: container1.id,
        children: children,
        competencies: [],
      });
      continue;
    }
  }
  return filtered;
};

export const filterSocleByContainerId = (socle, container1Id) => {
  for (const container1 of socle) {
    if (container1.id === container1Id) {
      return [container1];
    }
  }
  return [];
};

export const filterSocleByContainerIds = (
  socle,
  container1Id,
  container2Id
) => {
  for (const container1 of socle) {
    if (container1.id !== container1Id) {
      continue;
    }
    for (const container2 of container1.children) {
      if (container2.id === container2Id) {
        return [
          {
            id: container1.id,
            children: [container2],
            competencies: [],
          },
        ];
      }
    }
  }
  return [];
};
