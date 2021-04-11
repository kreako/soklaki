import { createStore } from "vuex";
import axios from "axios";
import { today } from "./utils/date";

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
    groupName: null,
    paymentOk: null,
    name: null,
    email: null,
    emailConfirmed: null,
  },
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
};

/// Return an object from an array
/// Initial array contains object with {id: ...}
/// Returned object contains a map id -> object
const fromArrayToIdObjects = (array) => {
  const obj = {};
  for (const idx in array) {
    const o = array[idx];
    obj[o.id] = o;
  }
  return obj;
};

const mutations = {
  setInError(state, error) {
    state.error.inError = error;
  },
  setErrorMessage(state, message) {
    state.error.message = message;
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
    { id, createdAt, updatedAt, date, text, userId, students, competencies }
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
    };
  },
  setObservationText(state, { id, text }) {
    state.observations[id].text = text;
  },
  setObservationDate(state, { id, date }) {
    state.observations[id].date = date;
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
};

const getters = {
  student: (state) => (studentId) => {
    const id = Number(studentId);
    if (id in state.students) {
      return state.students[id];
    } else {
      return {
        firstName: "",
        lastName: "",
        birthdate: "",
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
  async login({ commit }, { email, password }) {
    let answer = await axios.post("login", { email, password });
    commit("setLoginToken", answer.data.login.token);
    commit("setLoginErrorInvalid", answer.data.login.error);
    commit("setLoginUserId", answer.data.login.id);
    commit("setLoginGroupId", answer.data.login.group);
    commit("setLoginEmail", email);
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

  async students({ commit }) {
    let answer = await axios.get("students");
    commit("setStudents", answer.data.student);
  },

  async socle({ commit }) {
    let answer = await axios.get("socle");
    commit("setSocle", answer.data);
  },

  async insertObservation({ commit, state }, { text }) {
    let answer = await axios.post("insert-observation", {
      text: text,
      user_id: state.login.userId,
    });
    let data = answer.data.insert_eval_observation_one;
    commit("setObservation", {
      id: data.id,
      date: today(),
      createdAt: data.created_at,
      updatedAt: data.created_at,
      text: text,
      userId: state.login.userId,
      students: [],
      competencies: [],
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
    const answer = await axios.post("update-observation-date", {
      id: id,
      date: date,
    });

    let data = answer.data.update_eval_observation_by_pk;
    if (data == null) {
      throw new Error(`Quelque chose s'est mal passé dans la mise à jour de la date de l'observation. :(\n
        id: ${id}\n
        date: ${date}`);
    } else {
      commit("setObservationDate", {
        id: id,
        date: date,
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
