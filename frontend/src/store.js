import { createStore } from "vuex";
import axios from "axios";
import { dateJsObj, today, dateFromString } from "./utils/date";
import { searchOrCreatePeriod } from "./utils/period";
import { computeRanks } from "./utils/socle";

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
    email: null,
    invitation: {
      tokenValid: null,
      tokenTooOld: null,
    },
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
    templates: {},
    // Contains only id
    c1: [],
    c2: [],
    c3: [],
    c4: [],
  },
  // competencies id sorted by alpha rank directly from backend
  competenciesSorted: {
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
    store: {},
    // Array of id, sorted by date desc
    sorted: [],
  },
  comments: {
    // id -> comment object
    store: {},
    // Array of id, sorted by date desc
    sorted: [],
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
    // [{weekStart: "<date>", counts: [ { user: id, observations: count, evaluations: count} ... ] } ...]
    weeks: [],
  },
  reports: {
    // id -> reports
    store: {},
    // period_id -> student (sorted fullname)
    sorted: {},
  },
  // Single period/user report
  report: {
    observations: [],
    evaluations: [],
    comments: [],
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
      axios.defaults.headers.common["Authorization"] = `Bearer ${state.login.token}`;
      document.cookie = `token=${state.login.token}; SameSite=strict; Secure`;
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
  setLoginErrorInvitationTokenValid(state, valid) {
    state.login.invitation.tokenValid = valid;
  },
  setLoginErrorInvitationTokenTooOld(state, tooOld) {
    state.login.invitation.tokenTooOld = tooOld;
  },
  setLoginToken(state, token) {
    state.login.token = token;
    if (token) {
      localStorage.setItem("token", token);
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      document.cookie = `token=${state.login.token}; SameSite=strict; Secure`;
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
    state.socle.templates = fromArrayToIdObjects(socle.templates);
  },
  setCompetenciesSorted(state, competenciesSorted) {
    state.competenciesSorted = competenciesSorted;
  },
  setObservation(state, observation) {
    state.observation = observation;
  },
  setObservationText(state, { id, text }) {
    state.observation.text = text;
  },
  setObservationActive(state, { id, active }) {
    if (!active) {
      delete state.observations[id];
      const pos = state.sortedCreatedAtObservations.indexOf(id);
      state.sortedCreatedAtObservations.splice(pos, 1);
    } else {
      throw new Error("setObservationActive active=true not implemented");
    }
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
  setStats(state, { cycle, studentsCount, competenciesCount, stats, commentStats }) {
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
      weeks,
      observations,
      evaluations,
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

    // Now build weeks as :
    // [{weekStart: "<date>", counts: [ { user: id, observations: count, evaluations: count} ... ] } ...]
    // week start -> user id -> {observations: count, evaluations: count}
    const cache = {};
    for (const o of observations) {
      if (!(o.week_start in cache)) {
        cache[o.week_start] = {};
      }
      cache[o.week_start][o.user_id] = {
        observations: o.observations_count,
        evaluations: 0,
      };
    }
    for (const e of evaluations) {
      if (!(e.week_start in cache)) {
        cache[e.week_start] = {};
      }
      if (e.user_id in cache[e.week_start]) {
        cache[e.week_start][e.user_id].evaluations = e.evaluations_count;
      } else {
        cache[e.week_start][e.user_id] = {
          observations: 0,
          evaluations: e.evaluations_count,
        };
      }
    }

    for (const week of weeks) {
      const o = {};
      const start = dateFromString(week.week_start);
      o.weekStart = start;
      o.counts = [];
      if (week.week_start in cache) {
        let users = Object.keys(cache[week.week_start]);
        for (const userId of users) {
          const values = cache[week.week_start][userId];
          values.user = userId;
          o.counts.push(values);
        }
        // sort counts higher sum first
        o.counts.sort((a, b) => b.observations + b.evaluations - (a.observations + a.evaluations));
      }
      root.weeks.push(o);
    }
  },
  setEvaluations(state, evaluations) {
    state.evaluations.store = fromArrayToIdObjects(evaluations);
    state.evaluations.sorted = evaluations.map((x) => x.id);
  },
  setEvalComments(state, comments) {
    state.comments.store = fromArrayToIdObjects(comments);
    state.comments.sorted = comments.map((x) => x.id);
  },
  setReports(state, reports) {
    state.reports.store = fromArrayToIdObjects(reports);
    state.reports.sorted = {};
    for (const report of reports) {
      if (report.period != null) {
        if (!(report.period.eval_period_id in state.reports.sorted)) {
          state.reports.sorted[report.period.eval_period_id] = [];
        }
        state.reports.sorted[report.period.eval_period_id].push(report.id);
      }
    }
  },
  setReport(state, report) {
    state.report.observations = report.observations;
    state.report.evaluations = report.evaluations;
    state.report.comments = report.comments;
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
      period: null,
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
  containerById: (state) => (containerId) => {
    const id = Number(containerId);
    if (id in state.socle.containers) {
      return state.socle.containers[id];
    }
    return {
      full_rank: null,
      text: null,
      cycle: null,
      children: [],
      competencies: [],
    };
  },
  competencyById: (state) => (competencyId) => {
    const id = Number(competencyId);
    if (id in state.socle.competencies) {
      return state.socle.competencies[id];
    }
    return {
      full_rank: null,
      text: null,
      cycle: null,
    };
  },
  userById: (state) => (userId) => {
    const id = Number(userId);
    if (id in state.users) {
      return state.users[id];
    }
    return {
      email_confirmed: false,
      firstname: null,
      lastname: null,
      manager: false,
    };
  },
  periodById: (state) => (periodId) => {
    const id = Number(periodId);
    if (id != null && id in state.periods) {
      return state.periods[id];
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
    const id = Number(subjectId);
    if (id != null && id in state.socle.subjects) {
      return state.socle.subjects[id];
    }
    return {
      title: null,
    };
  },
  templateById: (state) => (templateId) => {
    const id = Number(templateId);
    if (id != null && id in state.socle.templates) {
      return state.socle.templates[id];
    }
    return {
      text: null,
    };
  },
  reportById: (state) => (reportId) => {
    const id = Number(reportId);
    if (id != null && id in state.reports.store) {
      return state.reports.store[id];
    }
    return {
      id: null,
      period: null,
      date: null,
      cycle: null,
      created_at: null,
      json_path: null,
      pdf_path: null,
      student_id: null,
    };
  },
  subjects: (state) => {
    const subjects = Object.values(state.socle.subjects);
    subjects.sort((a, b) => {
      const lowerA = a.title.toLowerCase();
      const lowerB = b.title.toLowerCase();
      if (lowerA < lowerB) {
        return -1;
      }
      if (lowerA > lowerB) {
        return 1;
      }
      return 0;
    });
    return subjects;
  },
};

axios.defaults.baseURL = import.meta.env.VITE_API_URL;

const actions = {
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

  async updateUserActive({ dispatch }, { id, active }) {
    await axios.post("update-user-active", { id, active });
    await dispatch("boot");
  },

  async login({ commit }, { email, password }) {
    const answer = await axios.post("login", { email, password });
    commit("setLoginToken", answer.data.login.token);
    commit("setLoginErrorInvalid", answer.data.login.error);
    commit("setLoginUserId", answer.data.login.id);
    commit("setLoginGroupId", answer.data.login.group_id);
    commit("setLoginEmail", email);
  },

  async logout({ commit }) {
    commit("setLoginToken", null);
    commit("setLoginUserId", null);
    commit("setLoginGroupId", null);
    commit("setLoginEmail", null);
    localStorage.clear();
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
    const answer = await axios.post("socle");
    commit("setSocle", answer.data);
  },

  async competenciesSorted({ commit }) {
    const answer = await axios.get("competencies/sorted");
    commit("setCompetenciesSorted", answer.data);
  },

  async insertObservation({ commit, state, dispatch }, { text }) {
    const date = today();
    await searchOrCreatePeriod(date, state, dispatch);
    const answer = await axios.post("insert-observation", {
      text: text,
      user_id: state.login.userId,
      date: date,
    });
    const data = answer.data.insert_eval_observation_one;
    commit("setObservation", data);
    return data.id;
  },

  async observation({ commit, state }, id) {
    const answer = await axios.post("observation", {
      id: id,
      group_id: state.login.groupId,
    });
    const data = answer.data.eval_observation_by_pk;
    if (data == null) {
      throw new Error(`Apparemment, je ne trouve pas cette observation : ${id}`);
    } else {
      commit("setObservation", data);
      commit("setPeriods", answer.data.periods);
      commit("setStudents", answer.data.students);
    }
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
      commit("setObservationsCount", answer.data.eval_observation_aggregate.aggregate.count);
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
      commit("setObservationsCount", answer.data.eval_observation_aggregate.aggregate.count);
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
      commit("setObservationsCount", answer.data.eval_observation_aggregate.aggregate.count);
    }
  },

  async updateGroupName({ commit }, { groupId, groupName }) {
    const answer = await axios.post("update-group-name", {
      group_id: groupId,
      name: groupName,
    });
    const data = answer.data.update_group_by_pk;
    if (data == null) {
      throw new Error(`La mise ?? jour du nom du groupe a ??chou?? :(\n
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

      weeks: data.weeks,
      observations: data.observations,
      evaluations: data.evaluations,
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
    return studentId;
  },

  async students({ commit, state }, { period, cycle, current }) {
    const answer = await axios.get("students", {
      params: {
        period: period,
        cycle: cycle,
        current: current,
      },
    });
    return answer.data;
  },

  async loadSocle({ state, dispatch }) {
    const answer = await axios.post("load-socle", {
      group_id: state.login.groupId,
    });
    const data = answer.data.load_socle;
    if (data.errorNonEmptySocle) {
      throw new Error("J'ai essay?? de recharger le socle mais il n'??tait pas vide !");
    }
    if (data.errorUnknownGroupId) {
      throw new Error("J'ai essay?? de recharger le socle mais je ne trouve pas votre groupe !");
    }
    if (data.errorUnknown) {
      throw new Error("J'ai essay?? de recharger le socle mais je n'ai pas r??ussi!");
    }
    // Now reload the socle
    await dispatch("socle");
  },

  async insertSocleContainer({ state, dispatch }, { containerId, cycle, rank, text }) {
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

  async insertSocleCompetency({ state, dispatch }, { containerId, cycle, rank, text }) {
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

  async insertSocleCompetencySubject({ state, dispatch }, { competencyId, subjectId }) {
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

  async updateSocleCompetencySubjectActive({ state, dispatch }, { id, active }) {
    await axios.post("update-socle-competency-subject-active", {
      id: id,
      active: active,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async deleteSocleCompetencySubject({ state, dispatch }, { subjectId, competencyId }) {
    await axios.post("delete-socle-competency-subject", {
      subject_id: subjectId,
      competency_id: competencyId,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleContainerContainerId({ state, dispatch }, { id, containerId }) {
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

  async updateSocleCompetencyContainerId({ state, dispatch }, { id, containerId }) {
    // Move this competency at the end of the current competencies
    // Find the future container
    const container = state.socle.containers[containerId];
    // Find it in the tree
    let c = null;
    if (container.container_id == null) {
      c = state.socle[container.cycle].find((x) => x.id == containerId);
    } else {
      c = state.socle[container.cycle]
        .find((x) => x.id == container.container_id)
        .children.find((x) => x.id == containerId);
    }
    const rank = c.competencies.length + 1;
    const { alphaFullRank, fullRank } = computeRanks({
      state,
      rank,
      containerId,
    });
    await axios.post("update-socle-competency-container-id", {
      id: id,
      rank: rank,
      alpha_full_rank: alphaFullRank,
      container_id: containerId,
      full_rank: fullRank,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleContainerRank({ state }, { id, rank }) {
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
  },

  async updateSocleCompetencyRank({ state }, { id, rank }) {
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

  async updateSocleCompetencyTemplateText({ dispatch }, { id, text }) {
    await axios.post("update-socle-competency-templates-text", {
      id,
      text,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async updateSocleCompetencyTemplateActive({ dispatch }, { id, active }) {
    await axios.post("update-socle-competency-templates-active", {
      id,
      active,
    });
    // Now reload the socle
    await dispatch("socle");
  },

  async insertSocleCompetencyTemplate({ state, dispatch }, { competencyId, text }) {
    await axios.post("insert-socle-competency-templates", {
      competency_id: competencyId,
      group_id: state.login.groupId,
      text: text,
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
      throw new Error(`Je n'ai pas r??ussi ?? cr??er cette p??riode :(\n
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
    { studentId, competencyId, date, status, comment }
  ) {
    await searchOrCreatePeriod(date, state, dispatch);
    const answer = await axios.post("insert-evaluation", {
      student_id: studentId,
      competency_id: competencyId,
      status: status,
      comment: comment,
      date: date,
      user_id: state.login.userId,
    });
    return answer.data.insert_eval_evaluation_one;
  },

  async insertComment({ commit, state, dispatch }, { date, studentId, text }) {
    const period = await searchOrCreatePeriod(date, state, dispatch);
    const answer = await axios.post("insert-comment", {
      date: date,
      student_id: studentId,
      text: text,
      user_id: state.login.userId,
    });
    await dispatch("evaluations", { periodId: period.id });
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
    await searchOrCreatePeriod(date, state, dispatch);
    await axios.post("update-comment-date", {
      id: id,
      date: date,
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
    await searchOrCreatePeriod(date, state, dispatch);
    await axios.post("update-evaluation-date", {
      id: id,
      date: date,
    });
    await dispatch("evaluations", { periodId });
  },

  async updateEvaluationComment({ dispatch }, { id, comment, periodId }) {
    await axios.post("update-evaluation-comment", { id, comment });
    await dispatch("evaluations", { periodId });
  },

  async updateEvaluationStatus({ dispatch }, { id, status, periodId }) {
    await axios.post("update-evaluation-status", { id, status });
    await dispatch("evaluations", { periodId });
  },

  async updateEvaluation({ state, dispatch }, { id, date, comment, status }) {
    await searchOrCreatePeriod(date, state, dispatch);
    await axios.post("update-evaluation", {
      id: id,
      date: date,
      comment: comment,
      status: status,
    });
  },

  async updateComment({ state, dispatch }, { id, date, text }) {
    const period = await searchOrCreatePeriod(date, state, dispatch);
    await axios.post("update-comment", {
      id: id,
      date: date,
      text: text,
    });
    // TODO not sure about period.id and periodId
    // OK for now but maybe in the future...
    await dispatch("evaluations", { periodId: period.id });
  },

  async reports({ commit }) {
    const answer = await axios.post("reports");
    const data = answer.data.report;
    commit("setReports", data);
  },

  async updateReportActive({ dispatch }, { id, active }) {
    await axios.post("update-report-active", { id, active });
    await dispatch("reports");
  },

  async report({ commit }, { periodId, studentId }) {
    const answer = await axios.post("report", {
      period_id: periodId,
      student_id: studentId,
    });
    const data = answer.data;
    commit("setReport", data);
  },

  async generateReport({}, { periodId, studentId }) {
    const answer = await axios.post("generate_report", {
      period_id: periodId,
      student_id: studentId,
    });
    const data = answer.data;
    return data;
  },

  async invitationGenerateToken({ state }) {
    const answer = await axios.post("invitation-generate-token", {
      user_id: state.login.userId,
      group_id: state.login.groupId,
    });
    return answer.data.invitation_generate_token.token;
  },

  async invitationVerifyToken({}, token) {
    const answer = await axios.post("invitation-verify-token", { token });
    return answer.data.invitation_verify_token;
  },

  async invitationSignupToken({ commit }, { token, email, password }) {
    const answer = await axios.post("invitation-signup-token", {
      token,
      email,
      password,
    });
    const data = answer.data.invitation_signup_token;
    commit("setLoginToken", data.token);
    commit("setLoginErrorKnownEmail", data.error_known_email);
    commit("setLoginErrorWeakPassword", data.error_weak_password);
    commit("setLoginUserId", data.user_id);
    commit("setLoginGroupId", data.group_id);
    commit("setLoginEmail", email);
    commit("setLoginErrorInvitationTokenValid", data.valid);
    commit("setLoginErrorInvitationTokenTooOld", data.too_old);
  },

  async countPerWeeks({}, { periodId }) {
    const answer = await axios.post("count-per-weeks", {
      period_id: periodId,
    });
    return answer.data;
  },

  async homeContent() {
    const answer = await axios.get("home_content/");
    return answer.data;
  },

  async statsByCycle({}, cycle) {
    const answer = await axios.get(`stats/${cycle}`);
    return answer.data;
  },

  async student({}, student_id) {
    const answer = await axios.get(`student/${student_id}`);
    return answer.data;
  },

  async saveStudentLastname({}, { id, lastname }) {
    const answer = await axios.post("student/lastname", {
      id: Number(id),
      lastname: lastname,
    });
    return answer.data;
  },

  async saveStudentFirstname({}, { id, firstname }) {
    const answer = await axios.post("student/firstname", {
      id: Number(id),
      firstname: firstname,
    });
    return answer.data;
  },

  async saveStudentBirthdate({}, { id, birthdate }) {
    const answer = await axios.post("student/birthdate", {
      id: Number(id),
      birthdate: birthdate,
    });
    return answer.data;
  },

  async saveStudentSchoolEntry({}, { id, schoolEntry }) {
    const answer = await axios.post("student/school_entry", {
      id: Number(id),
      school_entry: schoolEntry,
    });
    return answer.data;
  },

  async saveStudentSchoolExit({}, { id, schoolExit }) {
    const answer = await axios.post("student/school_exit", {
      id: Number(id),
      school_exit: schoolExit,
    });
    return answer.data;
  },

  async saveStudentActive({}, { id, active }) {
    const answer = await axios.post("student/active", {
      id: Number(id),
      active: active,
    });
    return answer.data;
  },

  async evaluationSingle({}, { studentId, competencyId }) {
    const answer = await axios.get(`evaluation/single/${studentId}/${competencyId}`);
    return answer.data;
  },

  async evaluationMulti({}, { competencyId }) {
    const answer = await axios.get(`evaluation/multi/${competencyId}`);
    return answer.data;
  },

  async evaluationNew({}, { studentId, competencyId, status, comment, date }) {
    const answer = await axios.post("evaluation/new", {
      student_id: Number(studentId),
      competency_id: Number(competencyId),
      status: status,
      comment: comment,
      date: date,
    });
    return answer.data;
  },

  async observationPrefill({}, { studentId, competencyId }) {
    const answer = await axios.get(`observation/prefill/${studentId}/${competencyId}`);
    return answer.data;
  },

  async observationNewPrefill({}, { studentId, competencyId, text }) {
    const answer = await axios.post("observation/new-prefill", {
      student_id: Number(studentId),
      competency_id: Number(competencyId),
      text: text,
    });
    return answer.data;
  },

  async evaluationStatsSummary() {
    const answer = await axios.get("eval_stats/summary");
    return answer.data;
  },

  async evaluationStatsByCycle({}, { cycle }) {
    const answer = await axios.get(`eval_stats/by_cycle/${cycle}`);
    return answer.data;
  },

  async observationSingle({}, { id }) {
    const answer = await axios.get(`observation/single/${id}`);
    return answer.data;
  },

  async updateObservationSingleText({}, { id, text }) {
    const answer = await axios.put("observation/single/text", {
      id: Number(id),
      text: text,
    });
    return answer.data;
  },

  async updateObservationSingleDate({ dispatch }, { id, date }) {
    await searchOrCreatePeriod(date, state, dispatch);
    const answer = await axios.put("observation/single/date", {
      id: Number(id),
      date: date,
    });
    return answer.data;
  },

  async insertObservationStudent({}, { observationId, studentId }) {
    const answer = await axios.put("observation/single/add-student", {
      observation_id: Number(observationId),
      student_id: studentId,
    });
    return answer.data;
  },

  async deleteObservationStudent({}, { studentId, observationId }) {
    const answer = await axios.put("observation/single/delete-student", {
      observation_id: Number(observationId),
      student_id: studentId,
    });
    return answer.data;
  },

  async insertObservationCompetency({ commit }, { observationId, competencyId }) {
    const answer = await axios.put("observation/single/add-competency", {
      observation_id: Number(observationId),
      competency_id: competencyId,
    });
    return answer.data;
  },

  async deleteObservationCompetency({ commit }, { observationId, competencyId }) {
    const answer = await axios.put("observation/single/delete-competency", {
      observation_id: Number(observationId),
      competency_id: competencyId,
    });
    return answer.data;
  },

  async setObservationActive({}, { id, active }) {
    const answer = await axios.post("observation/single/set-active", {
      id: Number(id),
      active: active,
    });
    return answer.data;
  },
};

const buildStore = () => {
  const store = createStore({
    state,
    mutations,
    actions,
    getters,
  });
  return store;
};

export const store = buildStore();
