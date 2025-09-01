const API_BASE = "http://127.0.0.1:8000";

const dateInput = document.getElementById("meal-date");
const planTable = document.getElementById("plan").querySelector("tbody");
const coursesDiv = document.getElementById("courses");

// --- Load meal plan for selected date ---
async function loadMealPlan(dateValue) {
  const res = await fetch(`${API_BASE}/mealplan/?selected_date=${dateValue}`);
  const data = await res.json();
  planTable.innerHTML = "";
  let total = 0;
  data.meals.forEach((m, idx) => {
    total += Number(m.kcal);
    const row = `<tr class="meal-${m.meal_category.toLowerCase()}">
      <td>${m.meal_category}</td>
      <td>${m.meal_type}</td>
      <td>${m.food_name}</td>
      <td>${m.servings}</td>
      <td>${m.kcal}</td>
    </tr>`;
    planTable.innerHTML += row;
  });
  document.getElementById("totalCalories").textContent = total;
}

// --- Load courses ---
async function loadCourses() {
  const res = await fetch(`${API_BASE}/courses`);
  const courses = await res.json();
  let html = "<ul>";
  courses.forEach(c => html += `<li>${c.title} - ${c.summary} (${c.level})</li>`);
  html += "</ul>";
  coursesDiv.innerHTML = html;
}

// --- Add Meal ---
document.getElementById("mealForm").addEventListener("submit", async e => {
  e.preventDefault();
  const formData = Object.fromEntries(new FormData(e.target));
  const res = await fetch(`${API_BASE}/add_meal/`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(formData)
  });
  const result = await res.json();
  alert(result.message);
  loadMealPlan(dateInput.value);
  e.target.reset();
});

// --- Add Course ---
document.getElementById("courseForm").addEventListener("submit", async e => {
  e.preventDefault();
  const formData = Object.fromEntries(new FormData(e.target));
  const res = await fetch(`${API_BASE}/add_course/`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(formData)
  });
  const result = await res.json();
  alert(result.message);
  loadCourses();
  e.target.reset();
});

// --- AI Meal Suggestions ---
document.getElementById("suggestBtn").addEventListener("click", async () => {
  const userId = 1;
  const dateValue = dateInput.value;
  const res = await fetch(`${API_BASE}/suggest_meal/?user_id=${userId}&meal_date=${dateValue}`);
  const data = await res.json();
  planTable.innerHTML = "";
  let total = 0;
  data.suggestions.forEach((m, idx) => {
    total += Number(m.kcal);
    planTable.innerHTML += `<tr class="meal-${m.meal_category.toLowerCase()}">
      <td>${m.meal_category}</td>
      <td>${m.meal_type}</td>
      <td>${m.food_name}</td>
      <td>${m.servings}</td>
      <td>${m.kcal}</td>
    </tr>`;
  });
  document.getElementById("totalCalories").textContent = total;
});

// --- Sport & Stadium selections ---
const sportsAndStadiums = [
  { sport: "Football", stadium: "Kasarani Stadium" },
  { sport: "Rugby", stadium: "RFUEA Ground" },
  { sport: "Cricket", stadium: "Mombasa Sports Club" },
  { sport: "Athletics", stadium: "Moi International Sports Centre" },
  { sport: "Basketball", stadium: "Safaricom Indoor Arena" },
  { sport: "Volleyball", stadium: "Kenyatta University Sports Hall" },
  { sport: "Hockey", stadium: "City Park Hockey Stadium" },
  { sport: "Tennis", stadium: "Nairobi Club Tennis Courts" },
  { sport: "Swimming", stadium: "Moi Sports Centre Aquatic Arena" },
  { sport: "Boxing", stadium: "Moi Indoor Stadium" }
];

const sportSelect = document.getElementById("sportSelect");
const stadiumSelect = document.getElementById("stadiumSelect");
const selectedPrefs = document.getElementById("selectedPrefs");
const selectPrefsBtn = document.getElementById("selectPreferencesBtn");

let userPrefs = { sport: '', stadium: '' };

// Populate selects
sportsAndStadiums.forEach(item => {
  const sportOption = document.createElement("option");
  sportOption.value = item.sport;
  sportOption.textContent = item.sport;
  sportSelect.appendChild(sportOption);

  const stadiumOption = document.createElement("option");
  stadiumOption.value = item.stadium;
  stadiumOption.textContent = item.stadium;
  stadiumSelect.appendChild(stadiumOption);
});

selectPrefsBtn.addEventListener('click', () => {
  userPrefs.sport = sportSelect.value;
  userPrefs.stadium = stadiumSelect.value;
  if(userPrefs.sport && userPrefs.stadium) {
    selectedPrefs.textContent = `Your favorite sport is ${userPrefs.sport} and your favorite stadium is ${userPrefs.stadium}.`;
  } else {
    selectedPrefs.textContent = 'Please select both sport and stadium.';
  }
});

// --- Initialize ---
window.onload = () => {
  const today = new Date().toISOString().slice(0,10);
  dateInput.value = today;
  loadMealPlan(today);
  loadCourses();
};
