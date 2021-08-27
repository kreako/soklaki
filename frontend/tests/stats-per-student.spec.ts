import { it, expect } from "./fixtures";

const FIRSTNAME = "Jimmy";
const LASTNAME = "Criquette";
const BIRTHDATE = "1987-02-13"; // so it is guaranteed in cycle 4
const SCHOOL_ENTRY = "2020-03-11";

it("is able to use stats per student to evaluate", async ({ page }) => {
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

  // student info
  await page.waitForSelector('"Prénom"');
  await page.waitForSelector(`"${FIRSTNAME}"`);
  await page.waitForSelector('"Nom"');
  await page.waitForSelector(`"${LASTNAME}"`);
  await page.waitForSelector('"Date d\'anniversaire"');
  await page.waitForSelector(`"${BIRTHDATE}"`);
  await page.waitForSelector("text=Date d'entrée à l'école");
  await page.waitForSelector(`"${SCHOOL_ENTRY}"`);
  await page.waitForSelector("text=L'élève est toujours à l'école");

  // statistics info
  await page.waitForSelector("text=Total0% >> :nth-match(div, 3)");
  await page.waitForSelector("text=Commentaire0% >> :nth-match(div, 3)");
  await page.waitForSelector("text=Observations0% >> :nth-match(div, 3)");
  await page.waitForSelector("text=Évaluations0% >> :nth-match(div, 3)");

  // Click on competency - modal appears
  await page.click("text=1.1.1.");
  await page.waitForSelector("text=Compétence - 1.1.1.");
  await page.waitForSelector(
    "text=1. interpréter des discours oraux complexes (distinguer implicite, explicit, comprendre divers types de récits)"
  );

  await page.click('button:has-text("OK")');

  // observation
  await Promise.all([
    page.waitForNavigation(),
    page.click("text=1.1.1.0 >> :nth-match(div, 2)"),
  ]);
  await page.waitForSelector(
    `text=Une nouvelle observation - 1.1.1. - ${FIRSTNAME} ${LASTNAME}`
  );
  await page.fill("textarea", "Mais oui !");
  await Promise.all([page.waitForNavigation(), page.click("text=Enregistrer")]);

  // Go back to the student page
  await page.goBack();
  await page.goBack();

  // Observation is now 1
  await page.waitForSelector("text=1.1.1.1 >> :nth-match(div, 2)");

  // Now evaluation
  await Promise.all([
    page.waitForNavigation(),
    page.click("text=1.1.1.1 >> :nth-match(a, 2)"),
  ]);

  // page content
  await page.waitForSelector(
    `text=Évaluation - 1.1.1. - ${FIRSTNAME} ${LASTNAME}`
  );
  await page.waitForSelector(
    "text=Cette évaluation n'a pas encore été mise à jour pour cette période."
  );
  await page.waitForSelector("text=1 observation");
  await page.waitForSelector("text=Mais oui !");

  // do it
  await page.fill("textarea", "Très bien");
  await page.click("text=Très bon");
  await page.waitForSelector("text=Très bonne maîtrise");
  await page.waitForSelector("text=Très bien");

  // Go to the next one
  await Promise.all([
    page.waitForNavigation(),
    page.click('[aria-label="Compétence suivante"] svg'),
  ]);

  // Check this is the next competency
  await page.waitForSelector(
    `text=Évaluation - 1.1.2. - ${FIRSTNAME} ${LASTNAME}`
  );

  // Go back to the student page
  await page.goBack();
  await page.goBack();

  // check colors for little stats square
  const element_obs = await page.waitForSelector(
    "text=1.1.1.1 >> :nth-match(a, 1)"
  );
  expect(
    (await element_obs.getAttribute("class")).includes("bg-green-500")
  ).toBeTruthy();

  const element_eval = await page.waitForSelector(
    "text=1.1.1.1 >> :nth-match(a, 2)"
  );
  expect(
    (await element_eval.getAttribute("class")).includes("bg-pink-500")
  ).toBeTruthy();
});
