from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles   # <- disabled for now
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from dotenv import load_dotenv
import os
import random

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "vitawellnessub")

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (commented out until you add a "static" folder)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Database connection
def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# ------------------- ROUTES -------------------

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/ping")
def ping():
    return {"message": "Backend is running on Railway!"}

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
    sql = """
        INSERT INTO meals (user_id, meal_date, meal_category, meal_type, food_name, servings, kcal)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
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
    sql = "INSERT INTO courses (title, summary, course_category, level) VALUES (%s, %s, %s, %s)"
    values = (course['title'], course['summary'], course['course_category'], course['level'])
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return {"message": "Course added successfully!"}

# Suggest meals (random from DB)
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
