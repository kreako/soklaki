import { dateJsObj } from "./date";

// Return a period from the periods list with period.start <= date <= period.end
// or null if not found
// date is in string format 'YYYY-MM-DD'
export const searchPeriod = (date, periods) => {
  if (date == null) {
    return null;
  }
  const dateValue = dateJsObj(date).valueOf();
  for (const periodId of Object.keys(periods)) {
    const period = periods[periodId];
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
