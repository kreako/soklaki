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

// TODO : trying to compensate for bisextile year
// But maybe 1 day, it will fail miserably
const YEARS_6 = 6 * 365 + 1;
const YEARS_9 = 9 * 365 + 2;
const YEARS_12 = 12 * 365 + 3;

export const estimateCycle = (birthdate, evaluationDate) => {
  if (birthdate == null || evaluationDate == null) {
    // Guard for init values
    return "";
  }
  // Convert to javascript date object
  birthdate = dateJsObj(birthdate);
  evaluationDate = dateJsObj(evaluationDate);

  // First estimate scholar year of the evaluation (first part)
  // If we are after july, the current year is the scholar year starting point
  // otherwise this was the year before
  const evaluationDateMonth = evaluationDate.getMonth() + 1;
  const evaluationDateYear = evaluationDate.getFullYear();
  const scholarYear =
    evaluationDateMonth > 7 ? evaluationDateYear : evaluationDateYear - 1;

  // Now, compute the date corresponding to the end of the year in the scholar year
  const endOfYear = new Date(scholarYear, 12, 31);
  const age = dateDiffInDays(endOfYear, birthdate);
  if (age < YEARS_6) {
    return "c1";
  } else if (age < YEARS_9) {
    return "c2";
  } else if (age < YEARS_12) {
    return "c3";
  } else {
    return "c4";
  }
};
