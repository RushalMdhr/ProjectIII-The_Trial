// src/services/api.js

import axios from "axios";


// =====================================================
// MOCK MODE
// =====================================================

// Keep this TRUE while we are developing without Django.
// Later your team will change this to false.
const USE_MOCK = true;


// =====================================================
// AXIOS CLIENT
// =====================================================

const client = axios.create({
  baseURL: "http://localhost:8000",
});


// =====================================================
// HELPER FUNCTIONS
// =====================================================

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}


// =====================================================
// TEMPORARY USERS DATABASE
// =====================================================

const USERS_KEY = "interviewai_users";


function getUsers() {
  const savedUsers = localStorage.getItem(USERS_KEY);

  if (!savedUsers) {
    return [];
  }

  return JSON.parse(savedUsers);
}


function saveUsers(users) {
  localStorage.setItem(
    USERS_KEY,
    JSON.stringify(users)
  );
}


// =====================================================
// ASK QUESTION
// =====================================================

export async function askQuestion(question) {

  if (USE_MOCK) {

    // Pretend we are waiting for the backend.
    await delay(800);

    const userQuestion = question
      .toLowerCase()
      .trim();


    // ---------------------------------------------
    // 2026 MOST ASKED QUESTIONS
    // ---------------------------------------------

    if (
      userQuestion.includes("2026") &&
      userQuestion.includes("most asked")
    ) {

      return {
        answer: [
          "1. Tell me about yourself and your background.",
          "2. Why should we hire you for this position?",
        ],
      };

    }


    // ---------------------------------------------
    // DEFAULT RESPONSE
    // ---------------------------------------------

    return {
      answer: [
        `I don't have specific data for "${question}" yet.`,
        "Try asking: What are the most asked questions in 2026?",
      ],
    };
  }


  // ---------------------------------------------
  // REAL DJANGO BACKEND — LATER
  // ---------------------------------------------

  const res = await client.post(
    "/interview/",
    {
      message: question,
    }
  );

  return res.data;
}


// =====================================================
// START INTERVIEW
// =====================================================

export async function startInterview(level) {

  if (USE_MOCK) {

    await delay(600);

    return {
      sessionId: "mock-session-1",
      level: level,
      firstQuestion:
        "Tell me about a project you're proud of.",
    };
  }


  const res = await client.post(
    "/interview/start",
    {
      level: level,
    }
  );

  return res.data;
}


// =====================================================
// SUBMIT ANSWER
// =====================================================

export async function submitAnswer(
  sessionId,
  answer
) {

  if (USE_MOCK) {

    await delay(700);

    return {
      feedback:
        "Solid answer — try to quantify the impact next time.",

      nextQuestion:
        "What was the hardest bug you fixed recently?",

      done: false,
    };
  }


  const res = await client.post(
    `/interview/${sessionId}/answer`,
    {
      answer: answer,
    }
  );

  return res.data;
}


// =====================================================
// REGISTER
// =====================================================

export async function register(
  name,
  email,
  password
) {

  if (USE_MOCK) {

    await delay(800);

    // Get existing users.
    const users = getUsers();


    // Check whether email already exists.
    const existingUser = users.find(
      (user) => user.email === email
    );


    if (existingUser) {

      return {
        success: false,
        message: "Email is already registered.",
      };

    }


    // Create new user.
    const newUser = {
      id: Date.now(),
      name: name,
      email: email,
      password: password,
    };


    // Add user.
    users.push(newUser);


    // Save users.
    saveUsers(users);


    return {
      success: true,
      message: "Registration successful!",

      user: {
        id: newUser.id,
        name: newUser.name,
        email: newUser.email,
      },
    };
  }


  // ---------------------------------------------
  // REAL DJANGO BACKEND — LATER
  // ---------------------------------------------

  const res = await client.post(
    "/auth/register",
    {
      name: name,
      email: email,
      password: password,
    }
  );

  return res.data;
}


// =====================================================
// LOGIN
// =====================================================

export async function login(
  email,
  password
) {

  if (USE_MOCK) {

    await delay(800);

    // Get registered users.
    const users = getUsers();


    // Find matching user.
    const user = users.find(
      (user) =>
        user.email === email &&
        user.password === password
    );


    // No user found.
    if (!user) {

      return {
        success: false,
        message: "Invalid email or password.",
      };

    }


    // User found.
    return {
      success: true,
      message: "Login successful!",

      user: {
        id: user.id,
        name: user.name,
        email: user.email,
      },
    };
  }


  // ---------------------------------------------
  // REAL DJANGO BACKEND — LATER
  // ---------------------------------------------

  const res = await client.post(
    "/auth/login",
    {
      email: email,
      password: password,
    }
  );

  return res.data;
}