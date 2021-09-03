import { it, expect } from "./fixtures";

const FIRSTNAME = "Aimé"; // starts with A so it is at the beginning
const LASTNAME = "Marcel";
const BIRTHDATE = "1983-02-13"; // so it is guaranteed in cycle 4
const SCHOOL_ENTRY = "2020-03-11";
const SCHOOL_EXIT = "2020-04-10"; // less than a month, it is short

it("is able to use stats per cycle to evaluate", async ({ page }) => {
  page.setDefaultTimeout(600000);
  await page.goto("http://127.0.0.1:3000/");
  await page.waitForFunction(() => document.title === "Accueil - soklaki.fr");

  await Promise.all([page.waitForNavigation(), page.click('"Élèves"')]);

  await Promise.all([
    page.waitForNavigation(),
    page.click('"Ajouter un élève"'),
  ]);

  await page.fill('input[type="text"]', FIRSTNAME);
  await page.fill(':nth-match(input[type="text"], 2)', LASTNAME);
  await page.fill(':nth-match(input[type="text"], 3)', BIRTHDATE);
  await page.fill(':nth-match(input[type="text"], 4)', SCHOOL_ENTRY);

  await Promise.all([page.waitForNavigation(), page.click("text=Sauvegarder")]);

  await page.waitForSelector('"Prénom"');
  await page.waitForSelector(`"${FIRSTNAME}"`);
  await page.waitForSelector('"Nom"');
  await page.waitForSelector(`"${LASTNAME}"`);
  await page.waitForSelector('"Date d\'anniversaire"');
  await page.waitForSelector(`"${BIRTHDATE}"`);
  await page.waitForSelector("text=Date d'entrée à l'école");
  await page.waitForSelector(`"${SCHOOL_ENTRY}"`);
  await page.waitForSelector("text=L'élève est toujours à l'école");

  await page.goto("http://127.0.0.1:3000/");
  await page.waitForFunction(() => document.title === "Accueil - soklaki.fr");

  // Click on cycle 4 box
  await Promise.all([page.waitForNavigation(), page.click("text=Cycle 4")]);

  // Check modal competency appearance
  await page.click("text=1.1.1.");
  await page.waitForSelector("text=Compétence - 1.1.1.");
  await page.waitForSelector(
    "text=1. interpréter des discours oraux complexes (distinguer implicite, explicit, comprendre divers types de récits)"
  );
  await page.click('button:has-text("OK")');

  // Check student is here
  await page.waitForSelector("text=Aimé Marcel");

  // Observation
  await Promise.all([
    page.waitForNavigation(),
    page.click(
      "tr:nth-child(2) td:nth-child(2) .block.ml-2 .bg-gray-500 .flex"
    ),
  ]);

  // Fill it
  await page.fill("textarea", "Mais oui");
  await Promise.all([page.waitForNavigation(), page.click("text=Enregistrer")]);

  // Go back to the stats page
  await page.goBack();
  await page.goBack();

  // Observation is now green with a 1
  const e = await page.waitForSelector(
    "tr:nth-child(2) td:nth-child(2) .block.ml-2 .bg-green-500 .flex"
  );
  expect(await e.innerText()).toBe("1");

  // Evaluation
  await Promise.all([
    page.waitForNavigation(),
    page.click("tr:nth-child(2) td:nth-child(3) .block.mr-2 .bg-gray-500"),
  ]);

  // Fill it
  await page.fill("textarea", "Oh oh");
  await page.click("text=Satisfaisant");

  // Go back to the stats page
  await page.goBack();

  // Evaluation is now green
  await page.waitForSelector(
    "tr:nth-child(2) td:nth-child(3) .block.mr-2 .bg-green-500"
  );

  // Now remove student from stats with SCHOOL_EXIT
  await Promise.all([page.waitForNavigation(), page.click('"Élèves"')]);

  await page.click(`"${FIRSTNAME} ${LASTNAME}"`);

  await page.click("text=Ajouter une date de sortie");
  await page.fill('input[type="text"]', SCHOOL_EXIT);
  await page.click("text=Sauvegarder");

  await page.goto("http://127.0.0.1:3000/");
  await page.waitForFunction(() => document.title === "Accueil - soklaki.fr");

  // Click on cycle 4 box
  await Promise.all([page.waitForNavigation(), page.click("text=Cycle 4")]);

  // Check student is not here anymore
  await page.waitForSelector("text=Aimé Marcel", { state: "hidden" });
});
