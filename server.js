const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// In-memory data store for live sales demo customization
let demoData = {
  clientName: "Globex Corp",
  solutionTitle: "Autonomous Cloud Migration",
  metrics: [
    { label: "Deployment Speed", value: "10x Faster", detail: "From weeks to minutes with Hermes and automated pipelines" },
    { label: "Operational Cost", value: "-42%", detail: "Optimized infrastructure and agentic code generation" },
    { label: "Client Satisfaction", value: "99.4%", detail: "Tailored real-time demos built specifically for stakeholder value" }
  ],
  testimonial: {
    quote: "This is the fastest proof-of-concept delivery we have ever witnessed in our enterprise sales cycle.",
    author: "Chief Technology Officer, Global Financial Services"
  }
};

app.get('/api/config', (req, res) => {
  res.json(demoData);
});

app.post('/api/config', (req, res) => {
  const { clientName, solutionTitle, metrics } = req.body;
  if (clientName) demoData.clientName = clientName;
  if (solutionTitle) demoData.solutionTitle = solutionTitle;
  if (metrics) demoData.metrics = metrics;
  res.json({ success: true, demoData });
});

app.listen(PORT, () => {
  console.log(`Sales Accelerator running on port ${PORT}`);
});
