/// Extract the date part from a date string
/// like 2021-03-30T17:59:16.637699+00:00
/// TODO maybe use Date() object from javascript ?
export const dateFromString = (dt) => {
  if (dt == null) {
    return "";
  }
  return dt.split("T")[0];
};

/// Build a date javascript object from a date string
/// like 2021-03-30T17:59:16.637699+00:00 or 2021-03-30
export const dateJsObj = (dt) => {
  // Not using Date.parse because as MDN states : Parsing of date strings
  // is strongly discouraged due to browser differences and inconsistencies.
  const year = dt.slice(0, 4);
  const month = dt.slice(5, 7);
  const day = dt.slice(8, 10);
  return new Date(year, month, day);
};

/// Diff to date and returns number of days
export const dateDiffInDays = (d1, d2) => {
  // In milliseconds
  const m1 = d1.valueOf();
  const m2 = d2.valueOf();
  const md = Math.abs(m1 - m2);
  // In seconds
  const s = md / 1000;
  // In minutes
  const m = s / 60;
  // In hours
  const h = m / 60;
  // In days
  return h / 24;
};
