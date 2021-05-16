import { folio as baseFolio } from "@playwright/test";
import { BrowserContextOptions } from "playwright";

const builder = baseFolio.extend();

builder.contextOptions.override(async ({ contextOptions }, runTest) => {
  const modifiedOptions: BrowserContextOptions = {
    ...contextOptions, // default options
    storageState: {
      origins: [
        {
          origin: "http://127.0.0.1:3000",
          localStorage: [
            { name: "userId", value: "469" },
            { name: "email", value: "test@integration.fr" },
            {
              name: "token",
              value:
                "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsidXNlciJdLCJ4LWhhc3VyYS1kZWZhdWx0LXJvbGUiOiJ1c2VyIiwieC1oYXN1cmEtdXNlci1pZCI6IjQ2OSIsIngtaGFzdXJhLXVzZXItZ3JvdXAiOiIzOTgifX0.tortdIhpSRrrXMkLxoaSdxYKGCCLkq0be5vbkKwIMI4",
            },
            { name: "groupId", value: "398" },
          ],
        },
      ],
    },
  };
  await runTest(modifiedOptions);
});

const folio = builder.build();

export const it = folio.it;
export const expect = folio.expect;
