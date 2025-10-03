const runDemoButton = document.getElementById("runDemo");
const resetButton = document.getElementById("resetDemo");
const status = document.getElementById("status");
const chatWindow = document.getElementById("chatWindow");
const ingestMeter = document.getElementById("ingestMeter");
const searchMeter = document.getElementById("searchMeter");
const responseMeter = document.getElementById("responseMeter");

const demoSteps = [
  {
    label: "Ingesting 52,048 enterprise documents...",
    meter: ingestMeter,
    width: "95%"
  },
  {
    label: "Vector search across HR + Finance indices...",
    meter: searchMeter,
    width: "88%"
  },
  {
    label: "Synthesizing grounded response with citations...",
    meter: responseMeter,
    width: "100%"
  }
];

const messages = [
  {
    role: "user",
    text: "Where are we seeing the highest retention risk this quarter?"
  },
  {
    role: "system",
    text:
      "Top risk signals originate from the APAC support org and mid-market sales pods. " +
      "Primary drivers include comp compression and reduced internal mobility. " +
      "Citations: HR/Retention-Q2.pdf, PeopleAnalytics/Attrition-Heatmap.xlsx."
  }
];

const resetDemo = () => {
  demoSteps.forEach((step) => {
    step.meter.style.width = "0%";
  });
  chatWindow.innerHTML =
    '<div class="chat-bubble system">Welcome. Press “Run Live Demo” to simulate an analyst response.</div>';
  status.textContent = "System ready. Awaiting demo run.";
};

const runDemo = async () => {
  resetDemo();
  status.textContent = "Booting retrieval pipeline...";

  for (const step of demoSteps) {
    await new Promise((resolve) => setTimeout(resolve, 700));
    step.meter.style.width = step.width;
    status.textContent = step.label;
  }

  await new Promise((resolve) => setTimeout(resolve, 600));
  status.textContent = "Response ready. Grounded citations attached.";

  messages.forEach((message, index) => {
    setTimeout(() => {
      const bubble = document.createElement("div");
      bubble.className = `chat-bubble ${message.role}`;
      bubble.textContent = message.text;
      chatWindow.appendChild(bubble);
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }, 400 * (index + 1));
  });
};

runDemoButton.addEventListener("click", runDemo);
resetButton.addEventListener("click", resetDemo);

resetDemo();
