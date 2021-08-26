import { it, expect } from "./fixtures";

const FIRSTNAME = "Charliet";
const LASTNAME = "LaChocolaterie";
const BIRTHDATE = "2003-08-13";
const SCHOOL_ENTRY = "2021-03-11";

it("is able to create a student", async ({ page }) => {
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
});
