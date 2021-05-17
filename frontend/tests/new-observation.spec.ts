import { it, expect } from "./fixtures";

it("is a basic test with the page", async ({ page }) => {
  await page.goto("http://127.0.0.1:3000/");
  await page.waitForFunction(() => document.title === "Accueil - soklaki.fr");
  await Promise.all([
    page.waitForNavigation(),
    page.click(':nth-match(:text("Nouvelle observation"), 2)'),
  ]);

  await page.waitForFunction(
    () => document.title === "Nouvelle observation - soklaki.fr"
  );
  await page.click("textarea");
  await page.fill("textarea", "C'est une observation très intéressante.");
  await Promise.all([page.waitForNavigation(), page.click("text=Enregistrer")]);

  await page.waitForFunction(
    () => document.title === "Observation - soklaki.fr"
  );
  await page.waitForSelector("text=C'est une observation très intéressante.");
  await page.waitForSelector("text=Non..."); // Not complete

  // Add student
  await page.click("text=Ajouter un élève");
  await page.click('button:has-text("Joan Meulou")');
  await page.waitForSelector("text=Joan Meulou (c1)");

  // Add a competency by click
  await page.click("text=Lier une compétence");
  await page.click(
    "text=4. Agir, s'exprimer, comprendre à travers l'activité physique"
  );
  await page.click(
    "text=2. Je cours, saute, lance de différentes façons, dans des espaces différents et "
  );
  await page.waitForSelector(
    "text=Je cours, saute, lance de différentes façons, dans des espaces différents et ave"
  );

  // Observation is now complete
  await page.waitForSelector("text=Oui !");

  // Add a competency by shortcut
  await page.click("text=Lier une compétence");
  await page.click('[placeholder="Filtre..."]');
  await page.fill('[placeholder="Filtre..."]', "2.1.8");
  await page.click("text=8. Je fais des petits calculs de tête (+1, -1 etc.)");
  await page.waitForSelector(
    "text=Je fais des petits calculs de tête (+1, -1 etc.)"
  );

  // Add a competency by search
  await page.click("text=Lier une compétence");
  await page.click('[placeholder="Filtre..."]');
  await page.fill('[placeholder="Filtre..."]', "respec");
  await page.click("text=10. Je respecte le matériel de l’école");
  await page.waitForSelector("text=Je respecte le matériel de l’école");

  // Fill an evaluation
  await page.click(
    "text=Évaluation2.1.8. Je fais des petits calculs de tête (+1, -1 etc.)Joan Meulou:Non >> :nth-match(button, 2)"
  );
  await page.click("textarea");
  await page.fill("textarea", "Oh oui, il court.");
  await page.click("text=Très bon");
  await page.waitForSelector("text=Très bonne maîtrise");

  // Add another student
  await page.click("text=Ajouter un élève");
  await page.click('button:has-text("Olivier Meu")');

  // Non complete again
  await page.waitForSelector("text=Non...");

  // Link a competency
  await page.click("text=cycle 4 - 1 élève Lier une compétence >> button");
  await page.click("text=2. Les méthodes et outils pour apprendre");
  await page.click("text=1. Organisation du travail personnel");
  await page.click("text=1. savoir comprendre des documents vidéo");

  // Complete again
  await page.waitForSelector("text=Oui !");

  // In competencies list
  await page.waitForSelector("text=savoir comprendre des documents vidéo");

  // In evaluation
  await page.waitForSelector(
    "text=2.1.1. savoir comprendre des documents vidéo"
  );
});
