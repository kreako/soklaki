import { it, expect } from "./fixtures";

it("is a basic test with the page", async ({ page }) => {
  await page.goto("http://127.0.0.1:3000/");
  const localStorage = await page.evaluate(() => localStorage)
  console.log(localStorage)
  const name = await page.innerText(".navbar__title");
  expect(name).toBe("Playwright");
});
