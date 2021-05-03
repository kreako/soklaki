import { searchPeriod, defaultPeriod } from "./period";

test("searchPeriod", () => {
  const periods = {
    1: {
      id: 1,
      start: "2019-08-29",
      end: "2020-07-11",
    },
    2: {
      id: 2,
      start: "2020-08-29",
      end: "2021-07-11",
    },
  };
  // inside
  let period = searchPeriod("2020-09-18", periods);
  expect(period.id).toBe(2);
  // end frontier
  period = searchPeriod("2020-07-11", periods);
  expect(period.id).toBe(1);
  // start frontier
  period = searchPeriod("2020-08-29", periods);

  // Not found cases
  expect(period.id).toBe(2);
  // in between
  expect(searchPeriod("2020-07-12", periods)).toBeNull();
  // before
  expect(searchPeriod("2019-08-28", periods)).toBeNull();
  // after
  expect(searchPeriod("2021-07-12", periods)).toBeNull();
});

test("defaultPeriod", () => {
  expect(defaultPeriod("2021-10-02")).toStrictEqual({
    name: "2021/2022 - S1",
    start: "2021-08-01",
    end: "2022-01-31",
  });
  expect(defaultPeriod("2021-08-01")).toStrictEqual({
    name: "2021/2022 - S1",
    start: "2021-08-01",
    end: "2022-01-31",
  });
  expect(defaultPeriod("2021-01-31")).toStrictEqual({
    name: "2020/2021 - S1",
    start: "2020-08-01",
    end: "2021-01-31",
  });
  expect(defaultPeriod("2021-02-01")).toStrictEqual({
    name: "2020/2021 - S2",
    start: "2021-02-01",
    end: "2021-07-31",
  });
  expect(defaultPeriod("2021-07-31")).toStrictEqual({
    name: "2020/2021 - S2",
    start: "2021-02-01",
    end: "2021-07-31",
  });
});
