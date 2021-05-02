import { computeRanks } from "./socle";

test("computeRanks with no parent", () => {
  const state = {};
  expect(
    computeRanks({ state: state, rank: 23, containerId: null })
  ).toStrictEqual({ alphaFullRank: "0023.", fullRank: "23." });
});

test("computeRanks with 1 parent", () => {
  const state = { containers: { 23: { container_id: null, rank: 3 } } };
  expect(
    computeRanks({ state: state, rank: 13, containerId: 23 })
  ).toStrictEqual({ alphaFullRank: "0003.0013.", fullRank: "3.13." });
});

test("computeRanks with 2 parent", () => {
  const state = {
    containers: {
      23: { container_id: 12, rank: 3 },
      12: { container_id: null, rank: 202 },
    },
  };
  expect(
    computeRanks({ state: state, rank: 14, containerId: 23 })
  ).toStrictEqual({ alphaFullRank: "0202.0003.0014.", fullRank: "202.3.14." });
});
