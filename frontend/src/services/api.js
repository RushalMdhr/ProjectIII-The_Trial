import axios from "axios";

// =====================================================
// MOCK MODE
// =====================================================

// Keep TRUE for now.
// When Django register/login APIs are ready,
// change this to FALSE.
const USE_MOCK = true;


// =====================================================
// AXIOS CLIENT
// =====================================================

const client = axios.create({
  baseURL: "http://localhost:8000",
});


// =====================================================
// JWT INTERCEPTOR
// =====================================================

client.interceptors.request.use(
  (config) => {

    const token = localStorage.getItem("accessToken");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);


// =====================================================
// HELPER
// =====================================================

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}


// =====================================================
// TEMPORARY MOCK USERS
// =====================================================

let mockUsers = [];


// =====================================================
// ASK QUESTION
// =====================================================

export async function askQuestion(question) {

  if (USE_MOCK) {

    await delay(800);

    const userQuestion = question
      .toLowerCase()
      .trim();

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

    return {
      answer: [
        `I don't have specific data for "${question}" yet.`,
        "Try asking: What are the most asked questions in 2026?",
      ],
    };
  }

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

  // ---------------------------------------------
  // MOCK REGISTER
  // ---------------------------------------------

  if (USE_MOCK) {

    await delay(800);

    // Check if email already exists
    const existingUser = mockUsers.find(
      (user) =>
        user.email.toLowerCase() ===
        email.toLowerCase()
    );

    if (existingUser) {

      return {
        success: false,
        message: "Email is already registered.",
      };

    }

    // Create temporary user
    const newUser = {
      id: Date.now(),
      name: name,
      email: email,
      password: password,
    };

    mockUsers.push(newUser);

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
  // REAL DJANGO BACKEND
  // ---------------------------------------------

  const res = await client.post(
    "/accounts/register/",
    {
      first_name: name,
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

  // ---------------------------------------------
  // MOCK LOGIN
  // ---------------------------------------------

  if (USE_MOCK) {

    await delay(800);

    const user = mockUsers.find(
      (user) =>
        user.email.toLowerCase() ===
        email.toLowerCase() &&
        user.password === password
    );

    if (!user) {

      return {
        success: false,
        message: "Invalid email or password.",
      };

    }

    return {
      success: true,
      message: "Login successful!",

      // Mock tokens for frontend testing
      access: "mock-access-token",
      refresh: "mock-refresh-token",

      user: {
        id: user.id,
        name: user.name,
        email: user.email,
      },
    };
  }


  // ---------------------------------------------
  // REAL DJANGO BACKEND
  // ---------------------------------------------

  const res = await client.post(
    "/accounts/login/",
    {
      email: email,
      password: password,
    }
  );

  return res.data;
}


// =====================================================
// GET CURRENT USER
// =====================================================

export async function getCurrentUser() {

  const res = await client.get(
    "/accounts/me/"
  );

  return res.data;
}


// =====================================================
// LOGOUT
// =====================================================

export function logout() {

  localStorage.removeItem("accessToken");
  localStorage.removeItem("refreshToken");
  localStorage.removeItem("currentUser");
}


// =====================================================
// TEST CONNECTION
// =====================================================

export async function testConnection(message) {

  const response = await fetch(
    "http://localhost:8000/test_connect",
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        message: message,
      }),
    }
  );

  return await response.json();
}