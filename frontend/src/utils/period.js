import { dateJsObj } from "./date";

// Return a period from the periods list with period.start <= date <= period.end
// or null if not found
// date is in string format 'YYYY-MM-DD'
export const searchPeriod = (date, periods) => {
  if (date == null) {
    return null;
  }
  const dateValue = dateJsObj(date).valueOf();
  for (const period of Object.values(periods)) {
    const startValue = dateJsObj(period.start).valueOf();
    if (dateValue < startValue) {
      // Not my period
      continue;
    }
    const endValue = dateJsObj(period.end).valueOf();
    if (dateValue > endValue) {
      // Not my period
      continue;
    }
    // my period !
    return period;
  }
  // default
  return null;
};

/// Return a "default" period object containing the date
export const defaultPeriod = (date) => {
  // default period is :
  // S1 : year-08-01 -> year+1-01-31
  // S2 : year+1-02-01 -> year+1-07-31
  const dt = dateJsObj(date);
  if (dt.getMonth() + 1 >= 8) {
    const year = dt.getFullYear();
    const start = `${year}-08-01`;
    const end = `${year + 1}-01-31`;
    const name = `${year}/${year + 1} - S1`;
    return { name, start, end };
  } else if (dt.getMonth() + 1 === 1) {
    const year = dt.getFullYear();
    const start = `${year - 1}-08-01`;
    const end = `${year}-01-31`;
    const name = `${year - 1}/${year} - S1`;
    return { name, start, end };
  } else {
    const year = dt.getFullYear();
    const start = `${year}-02-01`;
    const end = `${year}-07-31`;
    const name = `${year - 1}/${year} - S2`;
    return { name, start, end };
  }
};

export const searchOrCreatePeriod = async (date, state, dispatch) => {
  let p = searchPeriod(date, state.periods);
  if (p != null) {
    // Already found
    return p;
  }
  // Not found, create it
  const { name, start, end } = defaultPeriod(date);
  await dispatch("insertPeriod", { name, start, end });
  // Now it is here (insertPeriod does the reloading)
  p = searchPeriod(date, state.periods);
  return p;
};
