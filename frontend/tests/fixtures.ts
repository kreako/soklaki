import { folio as baseFolio } from "@playwright/test";
import { BrowserContextOptions } from "playwright";
import { readFile } from "fs/promises";

const builder = baseFolio.extend();

builder.contextOptions.override(async ({ contextOptions }, runTest) => {
  const content = await readFile("tests/signup-data.json", {
    encoding: "utf8",
  });
  const signupData = JSON.parse(content);
  const modifiedOptions: BrowserContextOptions = {
    ...contextOptions, // default options
    storageState: {
      origins: [
        {
          origin: "http://127.0.0.1:3000",
          localStorage: [
            { name: "userId", value: signupData.userId.toString() },
            { name: "email", value: signupData.email.toString() },
            { name: "token", value: signupData.token.toString() },
            { name: "groupId", value: signupData.groupId.toString() },
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
