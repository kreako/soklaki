import { createStore } from "vuex";
import axios from "axios";
import { dateJsObj, today } from "./utils/date";
import { searchPeriod } from "./utils/period";

const state = {
  error: {
    inError: false,
    message: "",
  },
  login: {
    error: {
      invalid: false,
      knownEmail: false,
      weakPassword: false,
    },
    userId: null,
    token: null,
    groupId: null,
    email: null,
  },
  group: {},
  users: [],
  // id -> period
  periods: {},
  // id sorted by end date desc
  sortedPeriods: [],
  // id -> student
  students: {},
  sortedStudents: [],
  socle: {
    // cache id -> object
    containers: {},
    competencies: {},
    subjects: {},
    // Contains only id
    c1: [],
    c2: [],
    c3: [],
    c4: [],
  },
  // id -> observation object
  observations: {},
  sortedCreatedAtObservations: [],
  evaluations: {
    // id -> evaluation object
    evaluations: {},
    // student_id -> competency_id -> evaluation_id
    byStudentCompetency: {},
  },
};

/// Return an object from an array
/// Initial array contains object with {id: ...}
/// Returned object contains a map id -> object
const fromArrayToIdObjects = (array) => {
  const obj = {};
  for (const idx in array) {
    const o = array[idx];
    obj[Number(o.id)] = o;
  }
  return obj;
};

const set_2_levels = (object, key1, key2, value) => {
  if (!(key1 in object)) {
    object[key1] = {};
  }
  object[key1][key2] = value;
};

const mutations = {
  setInError(state, error) {
    state.error.inError = error;
  },
  setErrorMessage(state, message) {
    state.error.message = message;
  },
  setGroup(state, group) {
    state.group = group;
  },
  setUsers(state, users) {
    state.users = fromArrayToIdObjects(users);
  },
  setPeriods(state, periods) {
    state.periods = fromArrayToIdObjects(periods);
    state.sortedPeriods = periods.map((x) => x.id);
  },
  loadFromLocalStorage(state) {
    state.login.email = localStorage.getItem("email");
    state.login.token = localStorage.getItem("token");
    state.login.userId = Number(localStorage.getItem("userId"));
    state.login.groupId = Number(localStorage.getItem("groupId"));
    if (state.login.token) {
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${state.login.token}`;
    }
  },
  setLoginEmail(state, email) {
    if (state.login.token != null) {
      // Meaning the login was successful, so store data
      localStorage.setItem("email", email);
    }
    state.login.email = email;
  },
  setLoginErrorInvalid(state, invalid) {
    state.login.error.invalid = invalid;
  },
  setLoginErrorKnownEmail(state, errorKnownEmail) {
    state.login.error.knownEmail = errorKnownEmail;
  },
  setLoginErrorWeakPassword(state, errorWeakPassword) {
    state.login.error.weakPassword = errorWeakPassword;
  },
  setLoginToken(state, token) {
    state.login.token = token;
    if (token) {
      localStorage.setItem("token", token);
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    }
  },
  setLoginUserId(state, userId) {
    if (state.login.token != null) {
      // Meaning the login was successful, so store data
      localStorage.setItem("userId", userId);
    }
    state.login.userId = userId;
  },
  setLoginGroupId(state, groupId) {
    if (state.login.token != null) {
      // Meaning the login was successful, so store data
      localStorage.setItem("groupId", groupId);
    }
    state.login.groupId = groupId;
  },
  setStudents(state, students) {
    state.students = fromArrayToIdObjects(students);
    state.sortedStudents = students.map((s) => s.id);
  },
  setSocle(state, socle) {
    state.socle.c1 = socle.c1;
    state.socle.c2 = socle.c2;
    state.socle.c3 = socle.c3;
    state.socle.c4 = socle.c4;
    // Now update cache
    state.socle.containers = fromArrayToIdObjects(socle.containers);
    state.socle.competencies = fromArrayToIdObjects(socle.competencies);
    state.socle.subjects = fromArrayToIdObjects(socle.subjects);
  },
  setObservation(
    state,
    {
      id,
      createdAt,
      updatedAt,
      date,
      text,
      userId,
      students,
      competencies,
      period,
    }
  ) {
    state.observations[id] = {
      id: id,
      createdAt: createdAt,
      updatedAt: updatedAt,
      userId: userId,
      date: date,
      text: text,
      students: students,
      competencies: competencies,
      period: period,
    };
  },
  setObservationText(state, { id, text }) {
    state.observations[id].text = text;
  },
  setObservationDate(state, { id, date, period }) {
    state.observations[id].date = date;
    state.observations[id].period = period;
  },
  insertObservationStudent(state, { id, observationId, studentId }) {
    state.observations[observationId].students.push({
      id: id,
      student_id: studentId,
    });
  },
  deleteObservationStudent(state, { observationId, id }) {
    let idx = 0;
    const length = state.observations[observationId].students.length;
    for (idx = 0; idx < length; idx++) {
      if (state.observations[observationId].students[idx].id === id) {
        break;
      }
    }
    state.observations[observationId].students.splice(idx, 1);
  },
  insertObservationCompetency(state, { id, observationId, competencyId }) {
    state.observations[observationId].competencies.push({
      id: id,
      competency_id: competencyId,
    });
  },
  setObservations(state, { data, limit, offset }) {
    // Remove everything that is already in there, that I'm currently trying to store
    state.sortedCreatedAtObservations.splice(
      offset,
      state.sortedCreatedAtObservations.length
    );
    // Now store
    for (const observation of data) {
      state.observations[observation.id] = observation;
      state.sortedCreatedAtObservations.push(observation.id);
    }
  },
  setGroupName(state, groupName) {
    state.group.name = groupName;
  },
  setUserName(state, { userId, firstname, lastname }) {
    state.users[userId].firstname = firstname;
    state.users[userId].lastname = lastname;
  },
  setEvaluationByStudentCompetency(
    state,
    { studentId, competencyId, evaluation }
  ) {
    if (evaluation == null) {
      set_2_levels(
        state.evaluations.byStudentCompetency,
        studentId,
        competencyId,
        null
      );
    } else {
      const evaluationId = evaluation.id;
      state.evaluations.evaluations[evaluationId] = evaluation;
      set_2_levels(
        state.evaluations.byStudentCompetency,
        studentId,
        competencyId,
        evaluationId
      );
    }
  },
};

const getters = {
  studentById: (state) => (studentId) => {
    const id = Number(studentId);
    if (id in state.students) {
      return state.students[id];
    } else {
      // Can happen when the store is not yet filled
      return {
        firstname: "",
        lastname: "",
        birthdate: "",
      };
    }
  },
  evaluationById: (state) => (evaluationId) => {
    const id = Number(evaluationId);
    if (id in state.evaluations.evaluations) {
      return state.evaluations.evaluations[id];
    } else {
      return {
        comment: null,
        created_at: null,
        status: "Empty",
        period: null,
        updated_at: null,
        user: { id: null },
        date: null,
        competency: { id: null },
      };
    }
  },
};

axios.defaults.baseURL = import.meta.env.VITE_API_URL;

const actions = {
  setError({ commit }, message) {
    commit("setInError", true);
    commit("setErrorMessage", message);
  },

  clearError({ commit }) {
    commit("setInError", false);
    commit("setErrorMessage", "");
  },

  async boot({ commit, state }) {
    let answer = await axios.post("boot", { group_id: state.login.groupId });
    commit("setGroup", answer.data.group[0]);
    commit("setUsers", answer.data.users);
    commit("setPeriods", answer.data.periods);
    commit("setStudents", answer.data.students);
  },

  async login({ commit }, { email, password }) {
    let answer = await axios.post("login", { email, password });
    commit("setLoginToken", answer.data.login.token);
    commit("setLoginErrorInvalid", answer.data.login.error);
    commit("setLoginUserId", answer.data.login.id);
    commit("setLoginGroupId", answer.data.login.group_id);
    commit("setLoginEmail", email);
    // Clear errors after login...
    commit("setInError", false);
    commit("setErrorMessage", "");
  },

  async signup({ commit }, { email, password }) {
    let answer = await axios.post("signup", { email, password });
    commit("setLoginToken", answer.data.signup.token);
    commit("setLoginErrorKnownEmail", answer.data.signup.errorKnownEmail);
    commit("setLoginErrorWeakPassword", answer.data.signup.errorWeakPassword);
    commit("setLoginUserId", answer.data.signup.id);
    commit("setLoginGroupId", answer.data.signup.group);
    commit("setLoginEmail", email);
  },

  async resetPassword({ commit }, { email }) {
    // TODO
    window.console.log("dev", import.meta.env.DEV);
    window.console.log("url", import.meta.env.VITE_API_URL);
  },

  async socle({ commit }) {
    let answer = await axios.get("socle");
    commit("setSocle", answer.data);
  },

  async insertObservation({ commit, state }, { text }) {
    const date = today();
    const period = searchPeriod(date, state.periods);
    const periodId = period == null ? null : period.id;
    let answer = await axios.post("insert-observation", {
      text: text,
      user_id: state.login.userId,
      date: date,
      eval_period_id: periodId,
    });
    let data = answer.data.insert_eval_observation_one;
    const periodObj = period == null ? null : { id: period.id };
    commit("setObservation", {
      id: data.id,
      date: date,
      createdAt: data.created_at,
      updatedAt: data.created_at,
      text: text,
      userId: state.login.userId,
      students: [],
      competencies: [],
      period: periodObj,
    });
    return data.id;
  },

  async observation({ commit }, id) {
    const answer = await axios.post("observation", { id: id });
    let data = answer.data.eval_observation_by_pk;
    if (data == null) {
      throw new Error(
        `Apparemment, je ne trouve pas cette observation : ${id}`
      );
    } else {
      commit("setObservation", {
        id: data.id,
        createdAt: data.created_at,
        updatedAt: data.updated_at,
        date: data.date,
        text: data.text,
        userId: data.user_id,
        students: data.students,
        competencies: data.competencies,
        period: data.period,
      });
    }
  },

  async updateObservationText({ commit }, { id, text }) {
    const answer = await axios.post("update-observation-text", {
      id: id,
      text: text,
    });
    let data = answer.data.update_eval_observation_by_pk;
    if (data == null) {
      throw new Error(`Quelque chose s'est mal passé dans la mise à jour du texte de l'observation. :(\n
        id: ${id}\n
        text: ${text}`);
    } else {
      commit("setObservationText", {
        id: id,
        text: text,
      });
    }
  },

  async updateObservationDate({ commit }, { id, date }) {
    const period = searchPeriod(date, state.periods);
    const periodId = period == null ? null : period.id;
    const answer = await axios.post("update-observation-date", {
      id: id,
      date: date,
      eval_period_id: periodId,
    });

    let data = answer.data.update_eval_observation_by_pk;
    if (data == null) {
      throw new Error(`Quelque chose s'est mal passé dans la mise à jour de la date de l'observation. :(\n
        id: ${id}\n
        date: ${date}`);
    } else {
      const periodObj = period == null ? null : { id: period.id };
      commit("setObservationDate", {
        id: id,
        date: date,
        period: periodObj,
      });
    }
  },

  async insertObservationStudent({ commit }, { observationId, studentId }) {
    let answer = await axios.post("insert-observation-student", {
      observation_id: observationId,
      student_id: studentId,
    });
    if (answer.error) {
      // TODO
    }
    let data = answer.data.insert_eval_observation_student_one;
    if (data == null) {
      // TODO
    } else {
      commit("insertObservationStudent", {
        id: data.id,
        observationId: data.observation_id,
        studentId: data.student_id,
      });
    }
  },

  async deleteObservationStudent({ commit }, { id, observationId }) {
    let answer = await axios.post("delete-observation-student", {
      id: id,
    });
    if (answer.error) {
      // TODO
    }
    commit("deleteObservationStudent", {
      id: id,
      observationId: observationId,
    });
  },

  async insertObservationCompetency(
    { commit },
    { observationId, competencyId }
  ) {
    let answer = await axios.post("insert-observation-competency", {
      observation_id: observationId,
      competency_id: competencyId,
    });
    if (answer.error) {
      // TODO
    }
    let data = answer.data.insert_eval_observation_competency_one;
    if (data == null) {
      // TODO
    } else {
      commit("insertObservationCompetency", {
        id: data.id,
        observationId: data.observation_id,
        competencyId: data.competency_id,
      });
    }
  },

  async observations({ commit }, { limit, offset }) {
    const answer = await axios.post("observations-sorted-created-at", {
      limit: limit,
      offset: offset,
    });
    let data = answer.data.eval_observation;
    if (data == null) {
      // No observations maybe
    } else {
      commit("setObservations", { data: data, limit: limit, offset: offset });
    }
  },

  async updateGroupName({ commit }, { groupId, groupName }) {
    const answer = await axios.post("update-group-name", {
      group_id: groupId,
      name: groupName,
    });
    let data = answer.data.update_group_by_pk;
    if (data == null) {
      throw new Error(`La mise à jour du nom du groupe a échoué :(\n
        groupId: ${groupId}\n
        groupName: ${groupName}`);
    }
    commit("setGroupName", groupName);
  },

  async insertPeriod({ commit }, { groupId, name, start, end }) {
    const answer = await axios.post("insert-period", {
      group_id: groupId,
      name: name,
      start: start,
      end: end,
    });
    let data = answer.data.insert_eval_period_one;
    if (data == null) {
      throw new Error(`Je n'ai pas réussi à créer cette période :(\n
        groupId: ${groupId}\n
        name: ${name}\n
        start: ${start}\n
        end: ${end}`);
    }
    // Reload periods
    const answer2 = await axios.get("periods");
    commit("setPeriods", answer2.data.periods);
  },

  async saveUserName({ commit }, { userId, firstname, lastname }) {
    const answer = await axios.post("set-user-name", {
      user_id: userId,
      firstname: firstname,
      lastname: lastname,
    });
    commit("setUserName", {
      userId: userId,
      firstname: firstname,
      lastname: lastname,
    });
  },

  async evaluationByStudentCompetency(
    { commit, state },
    { studentId, competencyId }
  ) {
    // return evaluation id if any or null
    if (studentId in state.evaluations.byStudentCompetency) {
      if (competencyId in state.evaluations.byStudentCompetency[studentId]) {
        if (
          state.evaluations.byStudentCompetency[studentId][competencyId] != null
        ) {
          // Already in it \o/ : no need to fetch data
          return state.evaluations.byStudentCompetency[studentId][competencyId];
        }
      }
    }
    // Fetch data !
    const answer = await axios.post("evaluation-by-student-competency", {
      student_id: studentId,
      competency_id: competencyId,
    });
    const data = answer.data.eval_evaluation;
    commit("setEvaluationByStudentCompetency", {
      studentId: studentId,
      competencyId: competencyId,
      evaluation: data.length === 0 ? null : data[0],
    });
    return data.length === 0 ? null : data[0].id;
  },

  async insertEvaluation(
    { commit, state },
    { studentId, competencyId, periodId, date, status, comment }
  ) {
    let answer = await axios.post("insert-evaluation", {
      student_id: studentId,
      competency_id: competencyId,
      status: status,
      comment: comment,
      date: date,
      eval_period_id: periodId,
      user_id: state.login.userId,
    });
    const data = answer.data.insert_eval_evaluation_one;
    commit("setEvaluationByStudentCompetency", {
      studentId: studentId,
      competencyId: competencyId,
      evaluation: data,
    });
  },
};

const buildStore = () => {
  const store = createStore({
    state,
    mutations,
    actions,
    getters,
  });

  // Set error handler
  store.subscribeAction({
    error: (action, state, error) => {
      console.log(`error action ${action.type}`);
      console.log("action", action);
      console.error("error", error);
      console.error("response", error.response);
      const actionStr = JSON.stringify(action, null, 2);
      const errorProperties = Object.getOwnPropertyNames(error);
      errorProperties.push("stack");
      const errorStr = JSON.stringify(error, errorProperties, 2);
      const responseStr = JSON.stringify(error.response, null, 2);
      const message = `Action: ${actionStr}\nError: ${errorStr}\nResponse: ${responseStr}`;
      store.dispatch("setError", message);
      try {
        axios.post("insert-frontend-store-error", {
          user_id: state.login.userId,
          error: errorStr,
          action: actionStr,
          response: responseStr,
        });
      } catch (error) {
        // Not even able to post the error in backend :(
      }
    },
  });

  return store;
};

export const store = buildStore();
