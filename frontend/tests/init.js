import axios from "axios";
import { writeFile } from "fs/promises";

const EMAIL = "test@integration.fr";
const PASSWORD = "test@integration.fr";

const graphql = async (query, variables) => {
  const answer = await axios.post("", {
    query,
    variables,
  });
  if ("errors" in answer.data) {
    console.log(answer.data);
    throw new Error(`errors in answer:\n${answer.data}`);
  }
  return answer.data.data;
};

const rmTestGroup = async () => {
  let data = await graphql(
    `query { group(where: {users: {email: {_eq: "${EMAIL}"}}}) { id } }`,
    {}
  );
  for (const group of data.group) {
    const id = group.id;
    let data = await graphql(
      `mutation { delete_group_by_pk(id: ${id}) { id } }`,
      {}
    );
  }
};

const newTestUser = async () => {
  let data = await graphql(
    `mutation { signup(email: "${EMAIL}", password: "${PASSWORD}") { id group token } } `
  );
  return {
    userId: data.signup.id,
    groupId: data.signup.group,
    token: data.signup.token,
    email: EMAIL,
  };
};

const writeSignupData = async (fname, signupData) => {
  const content = JSON.stringify(signupData);
  await writeFile(fname, content);
};

const createStudent = async (
  groupId,
  firstname,
  lastname,
  birthdate,
  schoolEntry
) => {
  const birthdateStr = `${birthdate.getFullYear()}-${
    birthdate.getMonth() + 1
  }-${birthdate.getDate()}`;
  const schoolEntryStr = `${schoolEntry.getFullYear()}-${
    schoolEntry.getMonth() + 1
  }-${schoolEntry.getDate()}`;
  const data = await graphql(`
    mutation {
      insert_student_one(
        object: {
          active: true
          group_id: ${groupId}
          firstname: "${firstname}"
          lastname: "${lastname}"
          birthdate: "${birthdateStr}"
          school_entry: "${schoolEntryStr}"
        }
      ) {
        id
      }
    }
  `);
};

const createStudents = async (groupId) => {
  const today = new Date();

  // Joan Meulou C1
  const five_years_ago = new Date();
  five_years_ago.setDate(five_years_ago.getDate() - 5 * 360);
  await createStudent(
    groupId,
    "Joan",
    "Meulou",
    five_years_ago,
    new Date(2019, 8, 19)
  );

  // Olivier Meu C4
  const fifteen_years_ago = new Date();
  fifteen_years_ago.setDate(five_years_ago.getDate() - 15 * 360);
  await createStudent(
    groupId,
    "Olivier",
    "Meu",
    fifteen_years_ago,
    new Date(2019, 8, 17)
  );
};

export const main = async () => {
  console.log("Init integration test fixture");
  // Setup axios with admin power
  axios.defaults.headers.common["x-hasura-admin-secret"] =
    process.env.HASURA_GRAPHQL_ADMIN_SECRET;
  axios.defaults.baseURL = process.env.HASURA_GRAPHQL_ENDPOINT;

  // Delete previous test group if any
  await rmTestGroup();

  // Create new user
  let signupData = await newTestUser();

  // Write signup data for future use in tests
  await writeSignupData("tests/signup-data.json", signupData);

  // Create a few students
  await createStudents(signupData.groupId);

  console.log("Done");
};

(async () => {
  await main();
})();
