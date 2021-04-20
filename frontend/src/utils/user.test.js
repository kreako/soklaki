import { userInitials } from "./user";

test("userInitials", () => {
  expect(userInitials({ firstname: "Babou", lastname: "meuh" })).toBe("BM");
  expect(userInitials({ firstname: null, lastname: "meuh" })).toBeNull();
  expect(userInitials({ firstname: "Babou", lastname: null })).toBeNull();
});
