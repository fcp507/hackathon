## Inspiration
MLB teams annually face the challenge of identifying future stars while avoiding draft busts. Inspired by the Moneyball revolution and the burgeoning field of AI-driven scouting, we embarked on creating Diamond AI—a system designed to revolutionize MLB prospect evaluation through cutting-edge AI techniques.

Our goal is to transform scouting into a more data-driven, predictive, and insightful process, uncovering hidden stars that might otherwise go unnoticed. Diamond AI seamlessly integrates with traditional prediction models, augmenting them with advanced AI capabilities. It features robust player comparison tools, allowing scouts to evaluate prospects against both historical and current player data for comprehensive analysis.

In the fast-paced environment of a hackathon, our team was motivated by the potential of AI to redefine the landscape of sports analytics. We built Diamond AI with the Plan and Execute agent, leveraging the capabilities of GenAI's large language models and agentic AI power. This integration enables us to process vast amounts of data and execute complex analytical tasks with precision. By utilizing GenAI Gemini from Google, we provide a powerful search tool that refines our evaluations and predictions, ensuring accuracy and depth in our insights.

The inspiration for Diamond AI also comes from the desire to harness AI's potential to uncover hidden talents—prospects who might be overlooked in traditional scouting processes. By integrating the latest AI advancements, we aim to set the stage for a new era of scouting—one that is deeply analytical, insightful, and capable of discovering the future stars of MLB.

Through this hackathon, Diamond AI serves as more than just a predictive tool; it is a testament to the transformative power of AI in sports analytics. By combining innovative AI technologies with the timeless excitement of baseball, we are paving the way for smarter, more informed decision-making in the world of MLB scouting.

## What It Does
Diamond AI is a multi-agent system that automates complete scouting workflows, powered by:
- ✅ LangGraph’s structured reasoning framework (Plan & Execute agents).
- ✅ Google Gemini 2’s advanced language and data-processing capabilities.
- ✅ Live data integration via Google Search, BigQuery, and mlb stats APIs.

For any MLB prospect, Diamond AI executes a multi-step agent workflow, including:
1. Gathering real-time player statistics (batting, pitching, fielding) from trusted sources.
2. Checking injury history using BigQuery and medical reports.
3. Analyzing performance trends (seasonal and game-by-game breakdowns) with the Gemini 2 Google search tool.
4. Comparing the prospect to similar MLB players using AI-driven historical analysis.
5. Predicting draft selection probability based on machine learning models.
6. Synthesizing all insights into a final scouting report, grounded in real-world data.

## How We Built It
🚀 **Tech Stack**:
- **LangGraph (Plan & Execute Agent)**: This framework is at the core of our AI's structured decision-making process, allowing us to dynamically generate and execute complex scouting workflows with precision and logic.
- **Google Gemini AI**: We leveraged Google Gemini AI for its powerful natural language processing capabilities, providing deep insights and enhanced scouting analysis through advanced language understanding.
- **Chainlit**: Interactive chat-based AI interface.
- **Flask**: Serving as our backend API, Flask enables efficient handling of data requests and responses, ensuring smooth communication between the user interface and the AI engine.
- **Jinja2**: This templating engine powers our player dashboard, offering dynamic content rendering and an organized presentation of player data and insights.
- **Google Cloud Platform (GCP)**: For scalability and reliability, we deployed Diamond AI on Google Cloud Platform, ensuring it can handle large data volumes and multiple user interactions simultaneously.
- **Big Query**: Historical MLB data analysis for pattern recognition.

![Plan and Execute Diagram](/agent.png)

The Plan & Execute agent was key—it dynamically generated step-by-step scouting workflows, ensuring the AI made structured and logical evaluations.

![Diamond AI](/diagram.png)

## Challenges We Faced
- **Grounding AI responses in real-world data**: Integrating live stats while maintaining accuracy.
- **Handling unstructured scouting reports**: Used LangChain document processing to extract key insights from text-based reports.
- **Cloud Deployment Issues**: Optimized API calls for real-time response speed.

## What We Learned
- Multi-step AI agents dramatically improve accuracy by structuring scouting workflows.
- Grounding AI responses in real-time data prevents hallucinations and increases reliability.
- A well-designed agent-based AI can automate complex workflows, saving time for MLB analysts.

## What’s Next?
- ⚾ Enhancing AI’s comparison models to better match prospects with MLB veterans.
- ⚾ Adding biomechanical video analysis for deeper scouting insights.
- ⚾ Expanding to minor league performance tracking for post-draft evaluations.

With Diamond AI, we’re bringing the future of AI-powered scouting to baseball.

## Why This Version?
- ✅ Fully integrates multi-step AI agents (LangGraph + Gemini 2).
- ✅ Emphasizes real-world data grounding (Google Search, BigQuery, APIs).
- ✅ Explains how structured AI workflows enhance MLB scouting.
- ✅ **Makes it clear that Diamond AI is a cutting-edge AI scouting assistant.**
