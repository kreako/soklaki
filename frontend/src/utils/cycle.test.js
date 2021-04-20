// const cycle = require("./cycle");
import { cycleFullName, cycleNb, estimateCycle } from "./cycle";

test("cycleNb", () => {
  expect(cycleNb("c1")).toBe("1");
  expect(cycleNb("c2")).toBe("2");
  expect(cycleNb("c3")).toBe("3");
  expect(cycleNb("c4")).toBe("4");
});

test("cycleFullName", () => {
  expect(cycleFullName("c1")).toBe("Cycle 1");
  expect(cycleFullName("c2")).toBe("Cycle 2");
  expect(cycleFullName("c3")).toBe("Cycle 3");
  expect(cycleFullName("c4")).toBe("Cycle 4");
});

test("estimateCycle", () => {
  // c1
  expect(estimateCycle("2015-11-02", "2020-12-31")).toBe("c1");
  expect(estimateCycle("2015-11-02", "2021-06-30")).toBe("c1");
  // c2
  expect(estimateCycle("2015-11-02", "2021-12-31")).toBe("c2");
  expect(estimateCycle("2015-11-02", "2022-06-30")).toBe("c2");
  expect(estimateCycle("2015-11-02", "2022-12-31")).toBe("c2");
  expect(estimateCycle("2015-11-02", "2023-06-30")).toBe("c2");
  expect(estimateCycle("2015-11-02", "2023-12-31")).toBe("c2");
  expect(estimateCycle("2015-11-02", "2024-06-30")).toBe("c2");
  // c3
  expect(estimateCycle("2015-11-02", "2024-12-31")).toBe("c3");
  expect(estimateCycle("2015-11-02", "2025-06-30")).toBe("c3");
  expect(estimateCycle("2015-11-02", "2025-12-31")).toBe("c3");
  expect(estimateCycle("2015-11-02", "2026-06-30")).toBe("c3");
  expect(estimateCycle("2015-11-02", "2026-12-31")).toBe("c3");
  expect(estimateCycle("2015-11-02", "2027-06-30")).toBe("c3");
  // c4
  expect(estimateCycle("2015-11-02", "2027-12-31")).toBe("c4");
  expect(estimateCycle("2015-11-02", "2028-06-30")).toBe("c4");
});
