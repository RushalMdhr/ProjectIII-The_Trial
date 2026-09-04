import axios from "axios";

// =====================================================
// AXIOS CLIENT
// =====================================================

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
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
// ASK QUESTION
// =====================================================

export async function askQuestion(question) {
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
  const response = await client.post(
    "/test_connect",
    { message }
  );

  return response.data;
}