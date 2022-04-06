import { dateFromString, dateJsObj, dateDiffInDays, today, dateToNiceString } from "./date";

test("dateFromString", () => {
  expect(dateFromString("2021-03-30T17:59:16.637699+00:00")).toBe("2021-03-30");
});

test("dateJsObj", () => {
  const d = dateJsObj("2021-03-30T17:59:16.637699+00:00");
  expect(d.getFullYear()).toBe(2021);
  expect(d.getMonth()).toBe(3 - 1);
  expect(d.getDate()).toBe(30);
});

test("dateJsObj error cases", () => {
  // separator 1
  expect(() => dateJsObj("2021/03-30T17:59:16.637699+00:00")).toThrow();
  // separator 2
  expect(() => dateJsObj("2021-03/30T17:59:16.637699+00:00")).toThrow();
  // year not a number
  expect(() => dateJsObj("abcd-03-30T17:59:16.637699+00:00")).toThrow();
  // year too small
  expect(() => dateJsObj("1374-03-30T17:59:16.637699+00:00")).toThrow();
  // year too big
  expect(() => dateJsObj("2642-03-30T17:59:16.637699+00:00")).toThrow();
  // month not a number
  expect(() => dateJsObj("2021-ab-30T17:59:16.637699+00:00")).toThrow();
  // month too small
  expect(() => dateJsObj("2021-00-30T17:59:16.637699+00:00")).toThrow();
  // month too big
  expect(() => dateJsObj("2021-13-30T17:59:16.637699+00:00")).toThrow();
  // day not a number
  expect(() => dateJsObj("2021-03-a0T17:59:16.637699+00:00")).toThrow();
  // day too small
  expect(() => dateJsObj("2021-03-00T17:59:16.637699+00:00")).toThrow();
  // day too big
  expect(() => dateJsObj("2021-03-32T17:59:16.637699+00:00")).toThrow();
  // Stupid date
  expect(() => dateJsObj("2021-02-31T17:59:16.637699+00:00")).toThrow();
});

test("dateDiffInDays", () => {
  // 1 day
  expect(dateDiffInDays(new Date(2021, 3, 14), new Date(2021, 3, 15))).toBe(1);
  // 1 day even in the other direction
  expect(dateDiffInDays(new Date(2021, 3, 15), new Date(2021, 3, 14))).toBe(1);
  // 10 days
  expect(dateDiffInDays(new Date(2021, 3, 15), new Date(2021, 3, 25))).toBe(10);
  // 365 days
  expect(dateDiffInDays(new Date(2021, 0, 1), new Date(2022, 0, 1))).toBe(365);
});

test("today", () => {
  // This can fail if the test is run exactly at
  const t1 = new Date();
  // 00:00 here
  // Oh funny !
  const t2 = dateJsObj(today());
  expect(t1.getFullYear()).toBe(t2.getFullYear());
  expect(t1.getMonth()).toBe(t2.getMonth());
  expect(t1.getDate()).toBe(t2.getDate());
});

test("dateToNiceString", () => {
  expect(dateToNiceString("2021-03-30T17:59:16.637699+00:00")).toBe("le 2021-03-30 à 17:59");
  expect(dateToNiceString(null)).toBeNull();
});
