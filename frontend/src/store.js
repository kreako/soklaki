import { createStore } from "vuex";
import axios from "axios";

const state = {
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
  students: [],
  socle: {
    // cache id -> object
    domains: {},
    components: {},
    competencies: {},
    subjects: {},
    // Contains only id
    c1: [],
    c2: [],
    c3: [],
    c4: [],
  },
};

const mutations = {
  loadFromLocalStorage(state) {
    window.console.log("loadFromLocalStorage");
    state.login.email = localStorage.getItem("email");
    state.login.token = localStorage.getItem("token");
    state.login.userId = localStorage.getItem("userId");
    state.login.groupId = localStorage.getItem("groupId");
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
    state.students = students;
  },
  setSocle(state, socle) {
    state.socle.c1 = socle.c1;
    state.socle.c2 = socle.c2;
    state.socle.c3 = socle.c3;
    state.socle.c4 = socle.c4;
    // Now update cache
    state.socle.domains = {};
    for (const idx in socle.domains) {
      const domain = socle.domains[idx];
      state.socle.domains[domain.id] = domain;
    }
    state.socle.components = {};
    for (const idx in socle.components) {
      const component = socle.components[idx];
      state.socle.components[component.id] = component;
    }
    state.socle.competencies = {};
    for (const idx in socle.competencies) {
      const competency = socle.competencies[idx];
      state.socle.competencies[competency.id] = competency;
    }
    state.socle.subjects = {};
    for (const idx in socle.subjects) {
      const subject = socle.subjects[idx];
      state.socle.subjects[subject.id] = subject;
    }
  },
};

axios.defaults.baseURL = import.meta.env.VITE_API_URL;

const actions = {
  async login({ commit }, { email, password }) {
    let answer = await axios.post("login", { email, password });
    window.console.log("answer", answer);
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
    window.console.log(data.id, data.created_at);
  },
};

export const store = createStore({
  state,
  mutations,
  actions,
});
