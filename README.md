# Code_Resune: AI-Powered Resume Optimization

Code_Resune is an intelligent resume optimization tool that uses AI agents to analyze job descriptions, identify gaps in your resume, and provide tailored recommendations to improve your chances of landing interviews.

## Overview

This project uses the CrewAI framework to create a team of specialized AI agents that work together to:

1. Analyze job descriptions to extract key requirements
2. Compare your resume against these requirements to identify gaps
3. Generate recommendations for resume optimization
4. Create an enhanced version of your resume tailored to the job

## Features

- **Job Description Analysis**: Extracts technical skills, soft skills, qualifications, and responsibilities from job descriptions
- **Gap Analysis**: Identifies missing skills and experience in your resume compared to job requirements
- **Resume Optimization**: Provides actionable recommendations to improve your resume
- **Resume Transformation**: Creates an enhanced version of your resume tailored to the job

## Prerequisites

- Python 3.8+
- Google AI API key (for Gemini models)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/Code_Resune.git
   cd Code_Resune
   ```

2. Install the required packages:
   ```
   pip install crewai crewai-tools python-dotenv
   ```

3. Create a `.env` file in the project root directory with your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

1. Place your resume in PDF format in the project directory as `Resume.pdf`

2. Place the job description you want to target in a text file named `devops_job_desc.txt` (or update the filename in the code)

3. Run the main script:
   ```
   python main.py
   ```

4. The script will generate several JSON files with the analysis results:
   - `jd_analysis.json`: Detailed breakdown of the job description
   - `gap_analysis.json`: Analysis of gaps between your resume and the job requirements
   - `rag_analysis.json`: Resume optimization recommendations
   - `enhancement_analysis.json`: Enhanced version of your resume

## How It Works

The system uses four specialized AI agents:

1. **Job Description Analyst**: Analyzes job descriptions to extract key requirements
2. **Resume-JD Gap Analyst**: Compares your resume against job requirements to identify gaps
3. **Resume Optimization Coach**: Provides recommendations for resume improvement
4. **Resume Transformation Specialist**: Creates an enhanced version of your resume

These agents work sequentially, with each agent building on the work of the previous agents.

## Customization

You can customize the behavior of the agents by modifying their roles, goals, and instructions in the `main.py` file.

## Troubleshooting

- If you encounter errors related to the tools, make sure your PDF and text files are in the correct location and format
- Check that your Google API key is valid and has access to the Gemini models

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the agent framework
- Google for the Gemini models
