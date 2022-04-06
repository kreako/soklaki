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
  const trailing = dt.slice(10);
  if (separator1 !== "-") {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.
Exemple : 2015-02-11 ou 1871-03-18

Chaque élément séparé par un tiret '-'.

Ici, le premier séparateur n'est pas un tiret '-', mais ${separator1} (date: ${dt}) !`);
  }
  if (separator2 !== "-") {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.
Exemple : 2015-02-11 ou 1871-03-18

Chaque élément séparé par un tiret '-'.

Ici, le deuxième séparateur n'est pas un tiret '-', mais ${separator2} (date: ${dt}) !`);
  }
  if (!Number.isInteger(year) || year > 2500 || year < 1500) {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.
Exemple : 2015-02-11 ou 1871-03-18

Ici, l'année '${dt.slice(0, 4)}' ne me semble pas valide (date: ${dt}) !`);
  }
  if (!Number.isInteger(month) || month > 12 || month < 1) {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.
Exemple : 2015-02-11 ou 1871-03-18

Ici, le mois '${dt.slice(5, 7)}' ne me semble pas valide (date: ${dt}) !`);
  }
  if (!Number.isInteger(day) || day > 31 || day < 1) {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.
Exemple : 2015-02-11 ou 1871-03-18

Ici, le jour '${dt.slice(8, 10)}' ne me semble pas valide (date: ${dt}) !`);
  }
  if (trailing != "" && trailing[0] != "T") {
    // Ignore the case where this is an iso datetime with a 'T' as date/hours separation
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.
Exemple : 2015-02-11 ou 1871-03-18
    
Ici, il y a un caractère supplémentaire '${trailing}' et ce n'est pas valide (date: ${dt}) !`);
  }
  const date = new Date(year, month - 1, day);
  if (year !== date.getFullYear() || month !== date.getMonth() + 1 || day !== date.getDate()) {
    throw new Error(`Le format de la date est <année:4 chiffres>-<mois:2 chiffres>-<jour:2 chiffres>.
Exemple : 2015-02-11 ou 1871-03-18

Ici, la date ne me semble pas valide (date: ${dt}) ?`);
  }
  return new Date(year, month - 1, day);
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

/// Return a date in string format
/// like 2021-04-06
/// d is a Date
export const dateToString = (d) => {
  const year = d.getFullYear();
  const month = d.getMonth() + 1;
  const day = d.getDate();

  return `${year}-${month.toString().padStart(2, "0")}-${day.toString().padStart(2, "0")}`;
};

/// Return today date in string format
/// like 2021-04-06
export const today = () => {
  return dateToString(new Date());
};

/// Return a string in french to display
/// dt is like 2021-03-30T17:59:16.637699+00:00
export const dateToNiceString = (dt) => {
  if (dt == null) {
    return null;
  }
  const [date, time] = dt.split("T");
  const reduceTime = time.slice(0, 5);
  return `le ${date} à ${reduceTime}`;
};

const MONTHS = {
  0: "Janvier",
  1: "Février",
  2: "Mars",
  3: "Avril",
  4: "Mai",
  5: "Juin",
  6: "Juillet",
  7: "Août",
  8: "Septembre",
  9: "Octobre",
  10: "Novembre",
  11: "Décembre",
};
/// Get month name from month number
/// month integer from 0 to 11 like Date API
export const monthName = (month) => MONTHS[month];

/// Return a list like : [{value: 0,text: "Janvier"}...]
export const months = () => {
  return Object.entries(MONTHS)
    .map(([value, text]) => {
      return { value: Number(value), text: text };
    })
    .sort((a, b) => a.value - b.value);
};
