import { useState } from "react";

type ChatResponse = {
  answer: string;
  citations: string[];
};

export default function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/v1/chat/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: "demo",
          question,
          top_k: 4
        })
      });
      const data = (await res.json()) as ChatResponse;
      setResponse(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ fontFamily: "Inter, sans-serif", padding: "2rem" }}>
      <h1>Conversational Intelligence Platform</h1>
      <p>Ask questions grounded in enterprise knowledge sources.</p>
      <div style={{ display: "flex", gap: "0.5rem" }}>
        <input
          style={{ flex: 1, padding: "0.75rem" }}
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="What are the latest retention risks?"
        />
        <button onClick={ask} disabled={loading || !question}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>
      {response && (
        <div style={{ marginTop: "1.5rem" }}>
          <h2>Answer</h2>
          <p>{response.answer}</p>
          <h3>Citations</h3>
          <ul>
            {response.citations.map((citation) => (
              <li key={citation}>{citation}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
