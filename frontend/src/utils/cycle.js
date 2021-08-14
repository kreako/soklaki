import { dateJsObj, dateDiffInDays } from "./date";

export const cycleNb = (cycle) => cycle[1];

export const cycleFullName = (cycle) => {
  if (cycle === "c1") {
    return "Cycle 1";
  } else if (cycle == "c2") {
    return "Cycle 2";
  } else if (cycle == "c3") {
    return "Cycle 3";
  } else if (cycle == "c4") {
    return "Cycle 4";
  } else {
    return null;
  }
};

export const cycleValid = (cycle) => {
  if (cycle[0] == "c") {
    if (
      cycle[1] == "1" ||
      cycle[1] == "2" ||
      cycle[1] == "3" ||
      cycle[1] == "4"
    ) {
      return true;
    }
  }
  return false;
};
