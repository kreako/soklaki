// const cycle = require("./cycle");
import { cycleFullName, cycleNb } from "./cycle";

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
