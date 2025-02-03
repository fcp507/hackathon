# Diamond AI - MLB Prospect Prediction

## Overview
Diamond AI is a cutting-edge MLB prospect prediction agent designed to analyze historical stats, injury data, scouting reports, and advanced prediction models to assess the potential success of MLB prospects. By leveraging various tools and models, Diamond AI provides comprehensive analysis and recommendations based on available data.

## Features
- **Player Data Analysis**: Retrieves and analyzes player statistics.
- **Injury History Assessment**: Evaluates injury histories and their potential impact.
- **Performance Insights**: Uses advanced statistics to assess player abilities.
- **Player Comparison**: Compares prospects with similar players.
- **Prediction Modeling**: Predicts player outcomes, including selection probability.
- **Responsive Web Interface**: Interactive UI for selecting players and viewing predictions.

## Inspiration
MLB teams annually face the challenge of identifying future stars while avoiding draft busts. Inspired by the Moneyball revolution and AI-driven scouting, we created Diamond AI—a system designed to revolutionize MLB prospect evaluation using cutting-edge AI techniques. Our goal is to make scouting more data-driven, predictive, and insightful, while also uncovering hidden stars that might otherwise be overlooked. Diamond AI integrates seamlessly with traditional prediction models, enhancing them with advanced AI capabilities. It features robust player comparison tools, allowing scouts to evaluate prospects against both historical and current player data for comprehensive analysis. To achieve even more advanced statistics and insights, we utilized GenAI Gemini from Google, providing a powerful search tool to refine our evaluations and predictions further.

## What It Does
Diamond AI is a multi-agent system that automates complete scouting workflows, powered by:
- ✅ LangGraph’s structured reasoning framework (Plan & Execute agents).
- ✅ Google Gemini 2’s advanced language and data-processing capabilities.
- ✅ Live data integration via Google Search, BigQuery, and third-party APIs.

For any MLB prospect, Diamond AI executes a multi-step workflow, including:
1. Gathering real-time player statistics (batting, pitching, fielding) from trusted sources.
2. Checking injury history using BigQuery and medical reports.
3. Analyzing performance trends (seasonal and game-by-game breakdowns) with the Gemini 2 Google search tool.
4. Comparing the prospect to similar MLB players using AI-driven historical analysis.
5. Predicting draft selection probability based on machine learning models.
6. Synthesizing all insights into a final scouting report, grounded in real-world data.

## How We Built It
🚀 **Tech Stack**:
- **LangGraph (Plan & Execute Agent)**: Structured AI decision-making.
- **Google Gemini AI**: Natural language & scouting insights.
- **Chainlit**: Interactive chat-based AI interface.
- **Flask**: Backend API.
- **Jinja2**: Player dashboard.
- **Google Cloud Platform (GCP)**: Scalable deployment.

The Plan & Execute agent was key—it dynamically generated step-by-step scouting workflows, ensuring the AI made structured and logical evaluations.

## Challenges We Faced
- **Real-Time Data Handling**: Integrating live stats while maintaining accuracy.
- **Scouting Complexity**: Balancing AI predictions with traditional scouting methodologies.
- **Cloud Deployment Issues**: Optimizing Chainlit + LangGraph on GCP.

## What We Learned
- LangGraph’s structured reasoning significantly improves AI decision-making.
- AI predictions must be paired with human scouting expertise for optimal results.
- A well-designed agent-based AI can automate complex workflows, saving time for MLB analysts.

## What’s Next?
- ⚾ Enhancing AI’s comparison models to better match prospects with MLB veterans.
- ⚾ Adding biomechanical video analysis for deeper scouting insights.
- ⚾ Expanding to minor league performance tracking for post-draft evaluations.

With Diamond AI, we’re bringing the future of AI-powered scouting to baseball.

## Installation
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/your-username/diamond-ai.git
   cd diamond-ai