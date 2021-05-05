import { createRouter, createWebHashHistory } from "vue-router";
import Login from "./pages/Login.vue";
import Signup from "./pages/Signup.vue";
import LostPassword from "./pages/LostPassword.vue";
import Home from "./pages/Home.vue";
import HomeContent from "./pages/HomeContent.vue";

const routes = [
  { path: "/login", component: Login },
  { path: "/lost-password", component: LostPassword },
  { path: "/signup", component: Signup },
  {
    path: "/",
    component: Home,
    children: [
      {
        path: "",
        component: HomeContent,
      },
      {
        path: "/new-observation",
        component: () => import("./pages/NewObservation.vue"),
      },
      {
        path: "/observation/:id",
        component: () => import("./pages/Observation.vue"),
      },
      {
        path: "/observations",
        component: () => import("./pages/Observations.vue"),
      },
      {
        path: "/first-step",
        component: () => import("./pages/FirstStep.vue"),
      },
      {
        path: "/students",
        component: () => import("./pages/Students.vue"),
      },
      {
        path: "/student/:id",
        component: () => import("./pages/Student.vue"),
      },
      {
        path: "/new-student",
        component: () => import("./pages/NewStudent.vue"),
      },
      {
        path: "/socle",
        component: () => import("./pages/Socle.vue"),
      },
      {
        path: "/stats",
        component: () => import("./pages/Stats.vue"),
      },
      {
        path: "/evaluations",
        component: () => import("./pages/Evaluations.vue"),
      },
      {
        path: "/evaluations-by-cycle/:cycle",
        component: () => import("./pages/EvaluationsByCycle.vue"),
      },
      {
        path: "/evaluation/:cycle/comment",
        component: () => import("./pages/EvaluationComment.vue"),
      },
      {
        path: "/evaluation/:cycle/:id",
        component: () => import("./pages/EvaluationCompetency.vue"),
      },
    ],
  },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes: routes,
});
