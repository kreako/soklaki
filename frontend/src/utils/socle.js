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
