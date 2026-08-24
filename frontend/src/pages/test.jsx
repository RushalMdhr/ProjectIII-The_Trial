import { useState } from "react";
import { testConnection } from "../services/api";

function Test() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = await testConnection(message);

    console.log(data);
    setResponse(data.message);
  };

  return (
    <div>
      <h1>Test Backend Connection</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter message"
        />

        <button type="submit">Send</button>
      </form>

      <p>Backend Response: {response}</p>
    </div>
  );
}

export default Test;