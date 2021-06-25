import {
  computeRanks,
  filterSocleBySubject,
  filterSocleBy2Ranks,
  filterSocleBy3Ranks,
  filterSocleByRegex,
  filterSocleByContainerId,
  filterSocleByContainerIds,
} from "./socle";

test("computeRanks with no parent", () => {
  const state = {};
  expect(
    computeRanks({ state: state, rank: 23, containerId: null })
  ).toStrictEqual({ alphaFullRank: "0023.", fullRank: "23." });
});

test("computeRanks with 1 parent", () => {
  const state = {
    socle: { containers: { 23: { container_id: null, rank: 3 } } },
  };
  expect(
    computeRanks({ state: state, rank: 13, containerId: 23 })
  ).toStrictEqual({ alphaFullRank: "0003.0013.", fullRank: "3.13." });
});

test("computeRanks with 2 parent", () => {
  const state = {
    socle: {
      containers: {
        23: { container_id: 12, rank: 3 },
        12: { container_id: null, rank: 202 },
      },
    },
  };
  expect(
    computeRanks({ state: state, rank: 14, containerId: 23 })
  ).toStrictEqual({ alphaFullRank: "0202.0003.0014.", fullRank: "202.3.14." });
});

test("filterSocleBySubject", () => {
  const socle = [
    {
      id: 23,
      children: [
        {
          id: 23,
          competencies: [{ id: 5, subjects: [{ id: 3, subject_id: 12 }] }],
        },
        {
          id: 12,
          competencies: [
            {
              id: 13,
              subjects: [
                {
                  id: 4,
                  subject_id: 14,
                },
              ],
            },
          ],
        },
        {
          id: 24,
          competencies: [
            {
              id: 5,
              subjects: [
                { id: 3, subject_id: 12 },
                { id: 5, subject_id: 13 },
              ],
            },
            {
              id: 6,
              subjects: [
                { id: 3, subject_id: 12 },
                { id: 5, subject_id: 14 },
              ],
            },
            {
              id: 5,
              subjects: [
                { id: 3, subject_id: 12 },
                { id: 5, subject_id: 13 },
              ],
            },
          ],
        },
      ],
      competencies: [],
    },
    {
      id: 24,
      children: [],
      competencies: [],
    },
    {
      id: 25,
      children: [],
      competencies: [
        {
          id: 5,
          subjects: [
            { id: 3, subject_id: 12 },
            { id: 5, subject_id: 13 },
          ],
        },
        {
          id: 6,
          subjects: [
            { id: 3, subject_id: 12 },
            { id: 5, subject_id: 14 },
          ],
        },
        {
          id: 5,
          subjects: [
            { id: 3, subject_id: 12 },
            { id: 5, subject_id: 13 },
          ],
        },
        {
          id: 6,
          subjects: [
            { id: 3, subject_id: 12 },
            { id: 5, subject_id: 14 },
          ],
        },
      ],
    },
  ];
  expect(filterSocleBySubject(socle, 14)).toStrictEqual([
    {
      id: 23,
      children: [
        {
          id: 12,
          competencies: [{ id: 13, subjects: [{ id: 4, subject_id: 14 }] }],
        },
        {
          id: 24,
          competencies: [
            {
              id: 6,
              subjects: [
                { id: 3, subject_id: 12 },
                { id: 5, subject_id: 14 },
              ],
            },
          ],
        },
      ],
      competencies: [],
    },
    {
      id: 25,
      children: [],
      competencies: [
        {
          id: 6,
          subjects: [
            { id: 3, subject_id: 12 },
            { id: 5, subject_id: 14 },
          ],
        },
        {
          id: 6,
          subjects: [
            { id: 3, subject_id: 12 },
            { id: 5, subject_id: 14 },
          ],
        },
      ],
    },
  ]);
});

test("filterSocleBy2Ranks", () => {
  const state = {
    socle: {
      containers: { 25: { rank: 19 }, 4: { rank: 23 } },
      competencies: { 5: { rank: 19 }, 6: { rank: 23 }, 3: { rank: 19 } },
    },
  };
  const socle = [
    {
      id: 25,
      children: [],
      competencies: [
        { id: 5, subjects: [] },
        { id: 6, subjects: [] },
      ],
    },
    {
      id: 4,
      children: [],
      competencies: [
        { id: 6, subjects: [] },
        { id: 3, subjects: [] },
      ],
    },
    {
      id: 3,
      children: [],
      competencies: [],
    },
  ];

  expect(filterSocleBy2Ranks(state, socle, 23, 19)).toStrictEqual([
    {
      id: 4,
      children: [],
      competencies: [{ id: 3, subjects: [] }],
    },
  ]);
});

test("filterSocleBy3Ranks", () => {
  const state = {
    socle: {
      containers: { 3: { rank: 3 }, 25: { rank: 19 }, 4: { rank: 23 } },
      competencies: { 5: { rank: 19 }, 6: { rank: 23 }, 3: { rank: 19 } },
    },
  };
  const socle = [
    {
      id: 4,
      children: [
        {
          id: 3,
          competencies: [{ id: 6, subjects: [] }],
        },
        {
          id: 25,
          competencies: [
            { id: 5, subjects: [] },
            { id: 6, subjects: [] },
          ],
        },
      ],
      competencies: [],
    },
  ];

  expect(filterSocleBy3Ranks(state, socle, 23, 19, 23)).toStrictEqual([
    {
      id: 4,
      children: [
        {
          id: 25,
          competencies: [{ id: 6, subjects: [] }],
        },
      ],
      competencies: [],
    },
  ]);
});

test("filterSocleByRegex", () => {
  const state = {
    socle: {
      competencies: {
        5: { text: "euh" },
        6: { text: "MeuH" },
        7: { text: " jdsqk" },
        8: { text: "ah oui MEuH bonjour" },
        9: { text: "ah oui M.EuH bonjour" },
      },
    },
  };
  const socle = [
    {
      id: 4,
      children: [
        {
          id: 3,
          competencies: [{ id: 7, subjects: [] }],
        },
        {
          id: 25,
          competencies: [
            { id: 5, subjects: [] },
            { id: 6, subjects: [] },
          ],
        },
      ],
      competencies: [],
    },
    {
      id: 3,
      children: [],
      competencies: [
        { id: 8, subjects: [] },
        { id: 9, subjects: [] },
      ],
    },
  ];

  let regex = new RegExp("meuh", "i");
  expect(filterSocleByRegex(state, socle, regex)).toStrictEqual([
    {
      id: 4,
      children: [
        {
          id: 25,
          competencies: [{ id: 6, subjects: [] }],
        },
      ],
      competencies: [],
    },
    {
      id: 3,
      children: [],
      competencies: [{ id: 8, subjects: [] }],
    },
  ]);
});

test("filterSocleByContainerId", () => {
  const socle = [
    {
      id: 3,
      children: [],
      competencies: [],
    },
    {
      id: 4,
      children: [
        {
          id: 3,
          competencies: [],
        },
        {
          id: 25,
          competencies: [],
        },
      ],
      competencies: [],
    },
    {
      id: 5,
      children: [],
      competencies: [],
    },
  ];
  expect(filterSocleByContainerId(socle, 4)).toStrictEqual([
    {
      id: 4,
      children: [
        {
          id: 3,
          competencies: [],
        },
        {
          id: 25,
          competencies: [],
        },
      ],
      competencies: [],
    },
  ]);
});

test("filterSocleByContainerIds", () => {
  const socle = [
    {
      id: 3,
      children: [],
      competencies: [],
    },
    {
      id: 4,
      children: [
        {
          id: 3,
          competencies: [],
        },
        {
          id: 25,
          competencies: [],
        },
        {
          id: 26,
          competencies: [],
        },
      ],
      competencies: [],
    },
    {
      id: 5,
      children: [],
      competencies: [],
    },
  ];
  expect(filterSocleByContainerIds(socle, 4, 25)).toStrictEqual([
    {
      id: 4,
      children: [
        {
          id: 25,
          competencies: [],
        },
      ],
      competencies: [],
    },
  ]);
});
