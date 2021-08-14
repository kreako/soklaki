import { cycleFullName, cycleNb, cycleValid } from "./cycle";

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

test("cycleValid", () => {
  expect(cycleValid("c1")).toBeTruthy();
  expect(cycleValid("c2")).toBeTruthy();
  expect(cycleValid("c3")).toBeTruthy();
  expect(cycleValid("c4")).toBeTruthy();

  expect(cycleValid("c0")).toBeFalsy();
  expect(cycleValid("c5")).toBeFalsy();
  expect(cycleValid("")).toBeFalsy();
  expect(cycleValid("e3")).toBeFalsy();
  expect(cycleValid("e")).toBeFalsy();
});
