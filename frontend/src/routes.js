import { createRouter, createWebHashHistory } from "vue-router";
import Login from "./pages/Login.vue";
import Signup from "./pages/Signup.vue";
import LostPassword from "./pages/LostPassword.vue";
import Home from "./pages/Home.vue";
import HomeContent from "./pages/HomeContent.vue";
import NewObservation from "./pages/NewObservation.vue";
import Observation from "./pages/Observation.vue";

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
        component: NewObservation,
      },
      {
        path: "/observation/:id",
        component: Observation,
      },
    ],
  },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes: routes,
});
