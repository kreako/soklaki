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
/// Throws errors (trying to be explicit if something is wrong)
export const dateJsObj = (dt) => {
  const year = Number(dt.slice(0, 4));
  const separator1 = dt[4];
  const month = Number(dt.slice(5, 7));
  const separator2 = dt[7];
  const day = Number(dt.slice(8, 10));
  if (separator1 !== "-") {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.\n
    Chaque élément séparé par un tiret '-'.\n
    Ici, le premier séparateur n'est pas un tiret '-', mais ${separator1} !`);
  }
  if (separator2 !== "-") {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.\n
    Chaque élément séparé par un tiret '-'.\n
    Ici, le deuxième séparateur n'est pas un tiret '-', mais ${separator2} !`);
  }
  if (!Number.isInteger(year) || year > 2100 || year < 1900) {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.\n
    Ici, l'année '${dt.slice(0, 4)}' ne me semble pas valide !`);
  }
  if (!Number.isInteger(month) || month > 12 || month < 1) {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.\n
    Ici, le mois '${dt.slice(5, 7)}' ne me semble pas valide !`);
  }
  if (!Number.isInteger(day) || day > 31 || day < 1) {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.\n
    Ici, le jour '${dt.slice(8, 10)}' ne me semble pas valide !`);
  }
  const date = new Date(year, month - 1, day);
  if (
    year !== date.getFullYear() ||
    month !== date.getMonth() + 1 ||
    day !== date.getDate()
  ) {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.\n
    Ici, la date ne me semble pas valide ?`);
  }
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

/// Return today date in string format
/// like 2021-04-06
export const today = () => {
  const d = new Date();
  const year = d.getFullYear();
  const month = d.getMonth() + 1;
  const day = d.getDate();

  return `${year}-${month
    .toString()
    .padStart(2, "0")}-${day.toString().padStart(2, "0")}`;
};
