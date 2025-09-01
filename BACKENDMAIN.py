from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import random

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MySQL
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="vitawellnessub"
    )

# Fetch all courses
@app.get("/courses")
def get_courses():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    db.close()
    return courses

# Fetch meals for a specific date
@app.get("/mealplan/")
def meal_plan(selected_date: str):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM meals WHERE meal_date=%s", (selected_date,))
    meals = cursor.fetchall()
    cursor.close()
    db.close()
    return {"meals": meals}

# Add a meal
@app.post("/add_meal/")
def add_meal(meal: dict):
    db = get_db()
    cursor = db.cursor()
    sql = "INSERT INTO meals (user_id, meal_date, meal_category, meal_type, food_name, servings, kcal) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    values = (
        meal['user_id'],
        meal['meal_date'],
        meal['meal_category'],
        meal.get('meal_type', meal['meal_category']),
        meal['food_name'],
        meal['servings'],
        meal['kcal']
    )
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Meal added successfully!"}

# Add a course
@app.post("/add_course/")
def add_course(course: dict):
    db = get_db()
    cursor = db.cursor()
    sql = "INSERT INTO courses (title, summary, course_category, level) VALUES (%s,%s,%s,%s)"
    values = (course['title'], course['summary'], course['course_category'], course['level'])
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Course added successfully!"}

# Suggest meals (AI / random from DB)
@app.get("/suggest_meal/")
def suggest_meal(user_id: int, meal_date: str):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM meals ORDER BY RAND() LIMIT 3")
    meals = cursor.fetchall()
    for meal in meals:
        meal['meal_type'] = meal.get('meal_category', 'Lunch')
    cursor.close()
    db.close()
    return {"suggestions": meals}
