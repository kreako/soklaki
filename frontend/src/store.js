import { createStore } from "vuex";
import axios from "axios";
import { dateJsObj, today } from "./utils/date";
import { searchOrCreatePeriod } from "./utils/period";
import { computeRanks } from "./utils/socle";

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
  // id of the current period
  currentPeriod: null,
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
  // Individual observation
  observation: { id: null },
  // id -> observation object
  observations: {},
  sortedCreatedAtObservations: [],
  // total number of observations in DB for the last query (user or incomplete or all)
  observationsCount: null,
  evaluations: {
    // id -> evaluation object
    evaluations: {},
    // id -> comment object
    comments: {},
    // Array of id, sorted by date desc
    sortedEvaluations: [],
    // Array of id, sorted by date desc
    sortedComments: [],
  },
  // stats for the selected period
  stats: {
    c1: {
      studentsCount: null,
      competenciesCount: null,
      // student id -> comments count
      commentsCount: {},
      // competency id -> student id -> { observations: count, evaluations: { count, status } }
      stats: {},
    },
    c2: {
      studentsCount: null,
      competenciesCount: null,
      // student id -> comments count
      commentsCount: {},
      // competency id -> student id -> { observations: count, evaluations: { count, status } }
      stats: {},
    },
    c3: {
      studentsCount: null,
      competenciesCount: null,
      // student id -> comments count
      commentsCount: {},
      // competency id -> student id -> { observations: count, evaluations: { count, status } }
      stats: {},
    },
    c4: {
      studentsCount: null,
      competenciesCount: null,
      // student id -> comments count
      commentsCount: {},
      // competency id -> student id -> { observations: count, evaluations: { count, status } }
      stats: {},
    },
  },
  statsSummary: {
    incompleteObservationsCount: null,
    c1: {
      studentsCount: null,
      competenciesCount: null,
      comments: {
        total: null,
        current: null,
      },
      observations: {
        total: null,
        current: null,
      },
      evaluations: {
        total: null,
        current: null,
      },
    },
    c2: {
      studentsCount: null,
      competenciesCount: null,
      comments: {
        total: null,
        current: null,
      },
      observations: {
        total: null,
        current: null,
      },
      evaluations: {
        total: null,
        current: null,
      },
    },
    c3: {
      studentsCount: null,
      competenciesCount: null,
      comments: {
        total: null,
        current: null,
      },
      observations: {
        total: null,
        current: null,
      },
      evaluations: {
        total: null,
        current: null,
      },
    },
    c4: {
      studentsCount: null,
      competenciesCount: null,
      comments: {
        total: null,
        current: null,
      },
      observations: {
        total: null,
        current: null,
      },
      evaluations: {
        total: null,
        current: null,
      },
    },
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
  setCurrentPeriod(state, period) {
    state.currentPeriod = period.id;
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
  setObservation(state, observation) {
    state.observation = observation;
  },
  setObservationText(state, { id, text }) {
    state.observation.text = text;
  },
  setObservations(state, { data, limit, offset }) {
    // Remove everything that is already in there
    // Component use pagination
    state.sortedCreatedAtObservations = [];
    // Now store
    for (const observation of data) {
      state.observations[observation.id] = observation;
      state.sortedCreatedAtObservations.push(observation.id);
    }
  },
  setObservationsCount(state, count) {
    state.observationsCount = count;
  },
  setGroupName(state, groupName) {
    state.group.name = groupName;
  },
  setUserName(state, { userId, firstname, lastname }) {
    state.users[userId].firstname = firstname;
    state.users[userId].lastname = lastname;
  },
  setStats(
    state,
    { cycle, studentsCount, competenciesCount, stats, commentStats }
  ) {
    const root = state.stats[cycle];
    root.studentsCount = studentsCount;
    root.competenciesCount = competenciesCount;
    for (const stat of commentStats) {
      root.commentsCount[Number(stat.student_id)] = stat.comments_count;
    }
    for (const stat of stats) {
      if (!(stat.competency_id in root.stats)) {
        root.stats[Number(stat.competency_id)] = {};
      }
      root.stats[Number(stat.competency_id)][Number(stat.student_id)] = {
        observations: stat.observations_count,
        evaluations: {
          count: stat.evaluations_count,
          status: stat.evaluation_status,
        },
      };
    }
  },
  setStatsSummary(
    state,
    {
      incompleteObservationsCount,
      studentsCountC1,
      competenciesCountC1,
      studentsCountC2,
      competenciesCountC2,
      studentsCountC3,
      competenciesCountC3,
      studentsCountC4,
      competenciesCountC4,
      comments,
      stats,
    }
  ) {
    const root = state.statsSummary;
    root.incompleteObservationsCount = incompleteObservationsCount;

    root.c1.studentsCount = studentsCountC1;
    root.c2.studentsCount = studentsCountC2;
    root.c3.studentsCount = studentsCountC3;
    root.c4.studentsCount = studentsCountC4;

    root.c1.competenciesCount = competenciesCountC1;
    root.c2.competenciesCount = competenciesCountC2;
    root.c3.competenciesCount = competenciesCountC3;
    root.c4.competenciesCount = competenciesCountC4;

    for (const comment of comments) {
      root[comment.cycle].comments.total = comment.total;
      root[comment.cycle].comments.current = comment.comments;
    }
    for (const stat of stats) {
      root[stat.cycle].observations.total = stat.total;
      root[stat.cycle].observations.current = stat.observations;
      root[stat.cycle].evaluations.total = stat.total;
      root[stat.cycle].evaluations.current = stat.evaluations;
    }
  },
  setEvaluations(state, evaluations) {
    state.evaluations.evaluations = fromArrayToIdObjects(evaluations);
    state.evaluations.sortedEvaluations = evaluations.map((x) => x.id);
  },
  setEvalComments(state, comments) {
    state.evaluations.comments = fromArrayToIdObjects(comments);
    state.evaluations.sortedComments = comments.map((x) => x.id);
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
        firstname: null,
        lastname: null,
        birthdate: null,
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
  observationById: (state) => (observationId) => {
    const id = Number(observationId);
    if (id in state.observations) {
      return state.observations[id];
    }
    return {
      date: null,
      created_at: null,
      updated_at: null,
      text: null,
      user_id: null,
      complete: null,
      competencies: [],
      students: [],
      period_id: null,
      complete: {
        complete: null,
      },
      competencies_aggregate: {
        aggregate: {
          count: null,
        },
      },
      students_aggregate: {
        aggregate: {
          count: null,
        },
      },
    };
  },
  competencyById: (state) => (competencyId) => {
    if (competencyId in state.socle.competencies) {
      return state.socle.competencies[competencyId];
    }
    return {
      full_rank: null,
      text: null,
      cycle: null,
    };
  },
  userById: (state) => (userId) => {
    if (userId in state.users) {
      return state.users[userId];
    }
    return {
      email_confirmed: false,
      firstname: null,
      lastname: null,
      manager: false,
    };
  },
  periodById: (state) => (periodId) => {
    if (periodId != null && periodId in state.periods) {
      return state.periods[periodId];
    }
    return {
      created_at: null,
      end: null,
      name: null,
      start: null,
      updated_at: null,
      students: [],
    };
  },
  subjectById: (state) => (subjectId) => {
    if (subjectId != null && subjectId in state.socle.subjects) {
      return state.socle.subjects[subjectId];
    }
    return {
      title: null,
    };
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
    const answer = await axios.post("boot", { group_id: state.login.groupId });
    commit("setGroup", answer.data.group[0]);
    commit("setUsers", answer.data.users);
    commit("setPeriods", answer.data.periods);
    if (answer.data.current_period.length > 0) {
      commit("setCurrentPeriod", answer.data.current_period[0]);
    }
    commit("setStudents", answer.data.students);
  },

  async login({ commit }, { email, password }) {
    const answer = await axios.post("login", { email, password });
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
    const answer = await axios.post("signup", { email, password });
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
    const answer = await axios.get("socle");
    commit("setSocle", answer.data);
  },

  async insertObservation({ commit, state, dispatch }, { text }) {
    const date = today();
    const period = await searchOrCreatePeriod(date, state, dispatch);
    const periodId = period == null ? null : period.id;
    const answer = await axios.post("insert-observation", {
      text: text,
      user_id: state.login.userId,
      date: date,
      eval_period_id: periodId,
    });
    const data = answer.data.insert_eval_observation_one;
    const periodObj = period == null ? null : { id: period.id };
    commit("setObservation", data);
    return data.id;
  },

  async observation({ commit }, id) {
    const answer = await axios.post("observation", { id: id });
    const data = answer.data.eval_observation_by_pk;
    if (data == null) {
      throw new Error(
        `Apparemment, je ne trouve pas cette observation : ${id}`
      );
    } else {
      commit("setObservation", data);
    }
  },

  async updateObservationText({ commit }, { id, text }) {
    const answer = await axios.post("update-observation-text", {
      id: id,
      text: text,
    });
    const data = answer.data.update_eval_observation_by_pk;
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

  async updateObservationDate({ commit, state, dispatch }, { id, date }) {
    const period = await searchOrCreatePeriod(date, state, dispatch);
    const answer = await axios.post("update-observation-date", {
      id: id,
      date: date,
      eval_period_id: period.id,
    });

    const data = answer.data.update_eval_observation_by_pk;
    if (data == null) {
      throw new Error(`Quelque chose s'est mal passé dans la mise à jour de la date de l'observation. :(\n
        id: ${id}\n
        date: ${date}`);
    } else {
      commit("setObservation", data);
    }
  },

  async insertObservationStudent({ commit }, { observationId, studentId }) {
    const answer = await axios.post("insert-observation-student", {
      observation_id: observationId,
      student_id: studentId,
    });
    const data = answer.data.insert_eval_observation_student_one.observation;
    commit("setObservation", data);
  },

  async deleteObservationStudent({ commit }, { studentId, observationId }) {
    const answer = await axios.post("delete-observation-student", {
      observation_id: observationId,
      student_id: studentId,
    });
    const data =
      answer.data.delete_eval_observation_student.returning[0].observation;
    commit("setObservation", data);
  },

  async insertObservationCompetency(
    { commit },
    { observationId, competencyId }
  ) {
    const answer = await axios.post("insert-observation-competency", {
      observation_id: observationId,
      competency_id: competencyId,
    });
    const data = answer.data.insert_eval_observation_competency_one.observation;
    commit("setObservation", data);
  },

  async deleteObservationCompetency(
    { commit },
    { observationId, competencyId }
  ) {
    const answer = await axios.post("delete-observation-competency", {
      observation_id: observationId,
      competency_id: competencyId,
    });
    const data =
      answer.data.delete_eval_observation_competency.returning[0].observation;
    commit("setObservation", data);
  },

  async observations({ commit, state }, { limit, offset }) {
    const answer = await axios.post("observations-sorted-created-at", {
      group_id: state.login.groupId,
      limit: limit,
      offset: offset,
    });
    const data = answer.data.eval_observation;
    if (data == null) {
      // No observations maybe
      // TODO
    } else {
      commit("setObservations", { data: data, limit: limit, offset: offset });
      commit(
        "setObservationsCount",
        answer.data.eval_observation_aggregate.aggregate.count
      );
    }
  },

  async observationsByUser({ commit, state }, { userId, limit, offset }) {
    const answer = await axios.post("observations-by-user", {
      group_id: state.login.groupId,
      user_id: userId,
      limit: limit,
      offset: offset,
    });
    const data = answer.data.eval_observation;
    if (data == null) {
      // No observations maybe
      // TODO ?
    } else {
      commit("setObservations", { data: data, limit: limit, offset: offset });
      commit(
        "setObservationsCount",
        answer.data.eval_observation_aggregate.aggregate.count
      );
    }
  },

  async observationsIncomplete({ commit, state }, { limit, offset }) {
    const answer = await axios.post("observations-incomplete", {
      group_id: state.login.groupId,
      limit: limit,
      offset: offset,
    });
    const data = answer.data.eval_observation;
    if (data == null) {
      // No observations maybe
      // TODO ?
    } else {
      commit("setObservations", { data: data, limit: limit, offset: offset });
      commit(
        "setObservationsCount",
        answer.data.eval_observation_aggregate.aggregate.count
      );
    }
  },

  async updateGroupName({ commit }, { groupId, groupName }) {
    const answer = await axios.post("update-group-name", {
      group_id: groupId,
      name: groupName,
    });
    const data = answer.data.update_group_by_pk;
    if (data == null) {
      throw new Error(`La mise à jour du nom du groupe a échoué :(\n
        groupId: ${groupId}\n
        groupName: ${groupName}`);
    }
    commit("setGroupName", groupName);
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

  async stats({ commit }, { periodId }) {
    const answer = await axios.post("stats", { period_id: periodId });
    // c1
    let studentsCount = answer.data.students_c1.aggregate.count;
    let competenciesCount = answer.data.competencies_c1.aggregate.count;
    let stats = answer.data.stats_c1;
    let commentStats = answer.data.comment_stats_c1;
    commit("setStats", {
      cycle: "c1",
      studentsCount,
      competenciesCount,
      stats,
      commentStats,
    });
    // c2
    studentsCount = answer.data.students_c2.aggregate.count;
    competenciesCount = answer.data.competencies_c2.aggregate.count;
    stats = answer.data.stats_c2;
    commentStats = answer.data.comment_stats_c2;
    commit("setStats", {
      cycle: "c2",
      studentsCount,
      competenciesCount,
      stats,
      commentStats,
    });
    // c3
    studentsCount = answer.data.students_c3.aggregate.count;
    competenciesCount = answer.data.competencies_c3.aggregate.count;
    stats = answer.data.stats_c3;
    commentStats = answer.data.comment_stats_c3;
    commit("setStats", {
      cycle: "c3",
      studentsCount,
      competenciesCount,
      stats,
      commentStats,
    });
    // c4
    studentsCount = answer.data.students_c4.aggregate.count;
    competenciesCount = answer.data.competencies_c4.aggregate.count;
    stats = answer.data.stats_c4;
    commentStats = answer.data.comment_stats_c4;
    commit("setStats", {
      cycle: "c4",
      studentsCount,
      competenciesCount,
      stats,
      commentStats,
    });
  },

  async statsSummary({ commit }, { periodId }) {
    const answer = await axios.post("stats-summary", { period_id: periodId });
    const data = answer.data;
    commit("setStatsSummary", {
      incompleteObservationsCount: data.incomplete_observations.aggregate.count,
      studentsCountC1: data.students_c1.aggregate.count,
      studentsCountC2: data.students_c2.aggregate.count,
      studentsCountC3: data.students_c3.aggregate.count,
      studentsCountC4: data.students_c4.aggregate.count,

      competenciesCountC1: data.competencies_c1.aggregate.count,
      competenciesCountC2: data.competencies_c2.aggregate.count,
      competenciesCountC3: data.competencies_c3.aggregate.count,
      competenciesCountC4: data.competencies_c4.aggregate.count,

      comments: data.comments,
      stats: data.stats,
    });
  },

  async insertStudent(
    { commit, state, dispatch },
    { birthdate, firstname, groupId, lastname, schoolEntry, schoolExit }
  ) {
    const answer = await axios.post("insert-student", {
      birthdate: birthdate,
      firstname: firstname,
      group_id: state.login.groupId,
      lastname: lastname,
      school_entry: schoolEntry,
      school_exit: schoolExit,
    });
    const studentId = answer.data.insert_student_one.id;
    // Reload students and periods
    await dispatch("students");
    return studentId;
  },

  async students({ commit, state }) {
    const answer = await axios.post("students", {
      group_id: state.login.groupId,
    });
    commit("setStudents", answer.data.students);
    commit("setPeriods", answer.data.periods);
    if (answer.data.current_period.length > 0) {
      commit("setCurrentPeriod", answer.data.current_period[0]);
    }
  },

  async updateStudentBirthdate({ commit, dispatch }, { studentId, birthdate }) {
    const answer = await axios.post("update-student-birthdate", {
      student_id: studentId,
      birthdate: birthdate,
    });
    // reload all students, a little bit too much - Maybe a TODO for the future me
    await dispatch("students");
  },

  async updateStudentFirstname({ commit, dispatch }, { studentId, firstname }) {
    const answer = await axios.post("update-student-firstname", {
      student_id: studentId,
      firstname: firstname,
    });
    // reload all students, a little bit too much - Maybe a TODO for the future me
    await dispatch("students");
  },

  async updateStudentLastname({ commit, dispatch }, { studentId, lastname }) {
    const answer = await axios.post("update-student-lastname", {
      student_id: studentId,
      lastname: lastname,
    });
    // reload all students, a little bit too much - Maybe a TODO for the future me
    await dispatch("students");
  },

  async updateStudentSchoolEntry(
    { commit, dispatch },
    { studentId, schoolEntry }
  ) {
    const answer = await axios.post("update-student-school-entry", {
      student_id: studentId,
      school_entry: schoolEntry,
    });
    // reload all students, a little bit too much - Maybe a TODO for the future me
    await dispatch("students");
  },

  async updateStudentSchoolExit(
    { commit, dispatch },
    { studentId, schoolExit }
  ) {
    const answer = await axios.post("update-student-school-exit", {
      student_id: studentId,
      school_exit: schoolExit,
    });
    // reload all students, a little bit too much - Maybe a TODO for the future me
    await dispatch("students");
  },

  async loadSocle({ state, dispatch }) {
    const answer = await axios.post("load-socle", {
      group_id: state.login.groupId,
    });
    const data = answer.data.load_socle;
    if (data.errorNonEmptySocle) {
      throw new Error(
        "J'ai essayé de recharger le socle mais il n'était pas vide !"
      );
    }
    if (data.errorUnknownGroupId) {
      throw new Error(
        "J'ai essayé de recharger le socle mais je ne trouve pas votre groupe !"
      );
    }
    if (data.errorUnknown) {
      throw new Error(
        "J'ai essayé de recharger le socle mais je n'ai pas réussi!"
      );
    }
    // Now reload the socle
    await dispatch("socle");
  },

  async insertSocleContainer(
    { state, dispatch },
    { containerId, cycle, rank, text }
  ) {
    const { alphaFullRank, fullRank } = computeRanks({
      state,
      rank,
      containerId,
    });
    await axios.post("insert-socle-container", {
      alpha_full_rank: alphaFullRank,
      container_id: containerId,
      cycle: cycle,
      full_rank: fullRank,
      group_id: state.login.groupId,
      rank: rank,
      text: text,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async insertSocleCompetency(
    { state, dispatch },
    { containerId, cycle, rank, text }
  ) {
    const { alphaFullRank, fullRank } = computeRanks({
      state,
      rank,
      containerId,
    });
    await axios.post("insert-socle-competency", {
      alpha_full_rank: alphaFullRank,
      container_id: containerId,
      cycle: cycle,
      full_rank: fullRank,
      group_id: state.login.groupId,
      rank: rank,
      text: text,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async insertSocleSubject({ state, dispatch }, { title }) {
    await axios.post("insert-socle-subject", {
      group_id: state.login.groupId,
      title: title,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async insertSocleCompetencySubject(
    { state, dispatch },
    { competencyId, subjectId }
  ) {
    await axios.post("insert-socle-competency-subject", {
      competency_id: competencyId,
      subject_id: subjectId,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleContainerActive({ state, dispatch }, { id, active }) {
    await axios.post("update-socle-container-active", {
      id: id,
      active: active,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleCompetencyActive({ state, dispatch }, { id, active }) {
    await axios.post("update-socle-competency-active", {
      id: id,
      active: active,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleSubjectActive({ state, dispatch }, { id, active }) {
    await axios.post("update-socle-subject-active", {
      id: id,
      active: active,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleCompetencySubjectActive(
    { state, dispatch },
    { id, active }
  ) {
    await axios.post("update-socle-competency-subject-active", {
      id: id,
      active: active,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleContainerContainerId(
    { state, dispatch },
    { id, containerId }
  ) {
    const rank = state.socle.containers[id].rank;
    const { alphaFullRank, fullRank } = computeRanks({
      state,
      rank,
      containerId,
    });
    await axios.post("update-socle-container-container-id", {
      id: id,
      alpha_full_rank: alphaFullRank,
      container_id: containerId,
      full_rank: fullRank,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleCompetencyContainerId(
    { state, dispatch },
    { id, containerId }
  ) {
    const rank = state.socle.competencies[id].rank;
    const { alphaFullRank, fullRank } = computeRanks({
      state,
      rank,
      containerId,
    });
    await axios.post("update-socle-competency-container-id", {
      id: id,
      alpha_full_rank: alphaFullRank,
      container_id: containerId,
      full_rank: fullRank,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleContainerRank({ state, dispatch }, { id, rank }) {
    const containerId = state.socle.containers[id].container_id;
    const { alphaFullRank, fullRank } = computeRanks({
      state,
      rank,
      containerId,
    });
    await axios.post("update-socle-container-rank", {
      id: id,
      alpha_full_rank: alphaFullRank,
      full_rank: fullRank,
      rank: rank,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleCompetencyRank({ state, dispatch }, { id, rank }) {
    const containerId = state.socle.competencies[id].container_id;
    const { alphaFullRank, fullRank } = computeRanks({
      state,
      rank,
      containerId,
    });
    await axios.post("update-socle-competency-rank", {
      id: id,
      alpha_full_rank: alphaFullRank,
      full_rank: fullRank,
      rank: rank,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleContainerText({ state, dispatch }, { id, text }) {
    await axios.post("update-socle-container-text", {
      id,
      text,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleCompetencyText({ state, dispatch }, { id, text }) {
    await axios.post("update-socle-competency-text", {
      id,
      text,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleSubjectText({ state, dispatch }, { id, title }) {
    await axios.post("update-socle-subject-text", {
      id,
      title,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async insertPeriod({ commit, state, dispatch }, { name, start, end }) {
    const answer = await axios.post("insert-period", {
      group_id: state.login.groupId,
      name: name,
      start: start,
      end: end,
    });
    const data = answer.data.insert_eval_period_one;
    if (data == null) {
      throw new Error(`Je n'ai pas réussi à créer cette période :(\n
        groupId: ${state.login.groupId}\n
        name: ${name}\n
        start: ${start}\n
        end: ${end}`);
    }
    // Reload periods
    await dispatch("periods");
  },

  async periods({ commit, state }) {
    const answer = await axios.post("periods", {
      group_id: state.login.groupId,
    });
    commit("setPeriods", answer.data.periods);
    if (answer.data.current_period.length > 0) {
      commit("setCurrentPeriod", answer.data.current_period[0]);
    }
  },

  async updatePeriodActive({ dispatch }, { id, active }) {
    await axios.post("update-period-active", { id, active });
    // Reload periods
    await dispatch("periods");
  },

  async updatePeriod({ dispatch }, { id, name, start, end }) {
    await axios.post("update-period", { id, name, start, end });
    await dispatch("periods");
  },

  async insertEvaluation(
    { commit, state, dispatch },
    { studentId, competencyId, periodId, date, status, comment }
  ) {
    const answer = await axios.post("insert-evaluation", {
      student_id: studentId,
      competency_id: competencyId,
      status: status,
      comment: comment,
      date: date,
      period_id: periodId,
      user_id: state.login.userId,
    });
    await dispatch("evaluations", { periodId });
  },

  async insertComment(
    { commit, state, dispatch },
    { periodId, date, studentId, text }
  ) {
    const period = await searchOrCreatePeriod(date, state, dispatch);
    const answer = await axios.post("insert-comment", {
      period_id: period.id,
      date: date,
      student_id: studentId,
      text: text,
      user_id: state.login.userId,
    });
    await dispatch("evaluations", { periodId });
  },

  async evaluations({ commit, state }, { periodId }) {
    const answer = await axios.post("evaluations", { period_id: periodId });
    commit("setEvaluations", answer.data.evaluations);
    commit("setEvalComments", answer.data.comments);
  },

  async updateCommentActive({ dispatch }, { id, active, periodId }) {
    await axios.post("update-comment-active", { id, active });
    await dispatch("evaluations", { periodId });
  },

  async updateCommentDate({ state, dispatch }, { id, date, periodId }) {
    const period = await searchOrCreatePeriod(date, state, dispatch);
    await axios.post("update-comment-date", {
      id: id,
      date: date,
      eval_period_id: period.id,
    });
    await dispatch("evaluations", { periodId });
  },

  async updateCommentText({ dispatch }, { id, text, periodId }) {
    await axios.post("update-comment-text", { id, text });
    await dispatch("evaluations", { periodId });
  },

  async updateEvaluationActive({ dispatch }, { id, active, periodId }) {
    await axios.post("update-evaluation-active", { id, active });
    await dispatch("evaluations", { periodId });
  },

  async updateEvaluationDate({ state, dispatch }, { id, date, periodId }) {
    const period = await searchOrCreatePeriod(date, state, dispatch);
    await axios.post("update-evaluation-date", {
      id: id,
      date: date,
      eval_period_id: period.id,
    });
    await dispatch("evaluations", { periodId });
  },

  async updateEvaluationComment({ dispatch }, { id, comment, periodId }) {
    await axios.post("update-comment-text", { id, comment });
    await dispatch("evaluations", { periodId });
  },

  async updateEvaluationStatus({ dispatch }, { id, status, periodId }) {
    await axios.post("update-comment-status", { id, status });
    await dispatch("evaluations", { periodId });
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
