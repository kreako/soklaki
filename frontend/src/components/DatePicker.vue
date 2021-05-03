<template>
  <div class="w-72 h-72 rounded-md border border-gray-300 shadow-sm px-2">
    <div class="flex flex-row">
      <button
        @click="goToYearSelect"
        class="text-xs text-gray-700 hover:text-teal-500"
      >
        {{ displayYear }}
      </button>
      <div class="flex-grow"></div>
      <button
        @click="selectToday"
        class="text-xs text-gray-700 hover:text-teal-500"
      >
        Aujourd'hui
      </button>
    </div>
    <div class="text-xl mb-2">
      {{ stringDate }}
    </div>
    <div v-if="mode === 'day'">
      <div class="flex flex-row items-center justify-between">
        <button @click="previousMonth" class="hover:text-teal-500">
          <IconChevronLeft class="h-4" />
        </button>
        <button @click="goToMonthSelect" class="hover:text-teal-500">
          {{ stringMonthYear }}
        </button>
        <button @click="nextMonth" class="hover:text-teal-500">
          <IconChevronRight class="h-4" />
        </button>
      </div>
      <div class="mt-2 grid grid-cols-7 justify-center content-center gap-y-1">
        <div
          v-for="header in ['L', 'M', 'M', 'J', 'V', 'S', 'D']"
          class="justify-self-center text-gray-400"
        >
          {{ header }}
        </div>
        <button
          v-for="day in days"
          @click="selectDay(day)"
          class="hover:text-teal-500 hover:bg-gray-100 rounded-full"
          :class="{ 'bg-gray-200': isSelected(day) }"
        >
          {{ day }}
        </button>
      </div>
    </div>
    <div v-if="mode === 'month'">
      <div class="flex flex-row items-center justify-between">
        <button @click="previousYear" class="hover:text-teal-500">
          <IconChevronLeft class="h-4" />
        </button>
        <button @click="goToYearSelect" class="hover:text-teal-500">
          {{ displayYear }}
        </button>
        <button @click="nextYear" class="hover:text-teal-500">
          <IconChevronRight class="h-4" />
        </button>
      </div>
      <div class="mt-4 grid grid-cols-3 justify-around gap-x-1 gap-y-2">
        <button
          v-for="m in monthsList"
          @click="selectMonth(m.value)"
          class="hover:bg-gray-100 hover:text-teal-500"
        >
          {{ m.text }}
        </button>
      </div>
    </div>
    <div v-if="mode === 'year'">
      <div class="flex flex-row items-center justify-between">
        <button @click="previousYearPlus" class="hover:text-teal-500">
          <IconChevronLeft class="h-4" />
        </button>
        <div>
          {{ displayYear }}
        </div>
        <button @click="nextYearPlus" class="hover:text-teal-500">
          <IconChevronRight class="h-4" />
        </button>
      </div>
      <div class="mt-4 grid grid-cols-5">
        <button
          v-for="y in yearsList"
          @click="selectYear(y)"
          class="hover:text-teal-500 hover:bg-gray-100"
        >
          {{ y }}
        </button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { defineProps, defineEmit, computed, ref } from "vue";
import { dateJsObj, dateToString, monthName, months } from "../utils/date";
import IconChevronLeft from "../icons/IconChevronLeft.vue";
import IconChevronRight from "../icons/IconChevronRight.vue";

const props = defineProps({
  value: String,
});

const valueDate = computed(() => {
  try {
    return dateJsObj(props.value);
  } catch (error) {
    // Not a valid date fallback to today
    return new Date();
  }
});

/// mode of the widget
/// day: to select a day
/// month: to select a month
/// year: to select a year
const mode = ref("day");

const year = ref(valueDate.value.getFullYear());
const month = ref(valueDate.value.getMonth());
const day = ref(valueDate.value.getDate());

const displayYear = ref(valueDate.value.getFullYear());
const displayMonth = ref(valueDate.value.getMonth());

const stringDate = computed(() =>
  dateToString(new Date(year.value, month.value, day.value))
);

const stringMonthYear = computed(
  () => `${monthName(displayMonth.value)} ${displayYear.value}`
);

/// Will return a list of list :
/// [[<number of monday>, <number of tuesday>...], [<number of monday>...], ]
/// With null padding
const days = computed(() => {
  const days = [];
  // let current = [];
  const currentDate = new Date(displayYear.value, displayMonth.value, 1);
  // Pad with null until the day (= 1)
  let day = 1;
  while (day != currentDate.getDay()) {
    // current.push(null);
    days.push(null);
    day = (day + 1) % 7;
  }
  // Now push until the month is ended
  while (currentDate.getMonth() === displayMonth.value) {
    //if (current.length === 7) {
    //days.push(current);
    //current = [];
    //}
    days.push(currentDate.getDate());
    currentDate.setDate(currentDate.getDate() + 1);
  }
  // push the last days of the month
  //if (current.length > 0) {
  //days.push(current);
  //}
  return days;
});

const emit = defineEmit(["selected"]);

const previousMonth = () => {
  if (displayMonth.value === 0) {
    // go to the last month of the previous year
    displayYear.value = displayYear.value - 1;
    displayMonth.value = 11;
  } else {
    displayMonth.value = displayMonth.value - 1;
  }
};

const nextMonth = () => {
  if (displayMonth.value === 11) {
    // go to the first month of the next year
    displayYear.value = displayYear.value + 1;
    displayMonth.value = 0;
  } else {
    displayMonth.value = displayMonth.value + 1;
  }
};

const goToYearSelect = () => {
  mode.value = "year";
};

const yearsList = computed(() => {
  return [...Array(25).keys()].map((x) => x + displayYear.value - 12);
});

const previousYearPlus = () => {
  displayYear.value = displayYear.value - 20;
};
const nextYearPlus = () => {
  displayYear.value = displayYear.value + 20;
};

const selectYear = (year) => {
  displayYear.value = year;
  mode.value = "month";
};

const goToMonthSelect = () => {
  mode.value = "month";
};

const previousYear = () => {
  displayYear.value = displayYear.value - 1;
};
const nextYear = () => {
  displayYear.value = displayYear.value + 1;
};

const monthsList = months();

const selectMonth = (month) => {
  displayMonth.value = month;
  mode.value = "day";
};

const selectDay = (_day) => {
  year.value = displayYear.value;
  month.value = displayMonth.value;
  day.value = _day;
  emit("selected", stringDate.value);
};

const selectToday = () => {
  const today = new Date();
  displayYear.value = today.getFullYear();
  displayMonth.value = today.getMonth();
  year.value = displayYear.value;
  month.value = displayMonth.value;
  day.value = today.getDate();
  emit("selected", stringDate.value);
};

const isSelected = (_day) => {
  if (displayYear.value !== year.value) {
    return false;
  }
  if (displayMonth.value !== month.value) {
    return false;
  }
  if (_day !== day.value) {
    return false;
  }
  return true;
};
</script>
