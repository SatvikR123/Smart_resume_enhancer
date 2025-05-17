"""
Broadly we have to create a resume optimizer tool that will take a resume and a job description as input and output a polished resume that is optimized for the job description. 

For this we have to create a crew of agents that will perform different tasks to optimize the resume.

The crew will be:
1. Job Description Analyst
2. Resume-JD Gap Analyst
3. Resume Optimization Coach
4. Resume Transformation Specialist

"""

# Importing necessary libraries
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import PDFSearchTool, TXTSearchTool
from dotenv import load_dotenv
import os
from os.path import join, dirname

# Configuirng the environment
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Setting up the LLM
llm = LLM(
    model="gemini/gemini-1.5-flash",  
    api_key=f"{GOOGLE_API_KEY}",  
    config={
        "provider": "gemini" 
    }
)

# Setting up the tools
# PDF Search Tool
resume_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Resume.pdf"))
pdf_search_tool = PDFSearchTool(
    pdf=resume_path,
    config=dict(
        llm=dict(
            provider="google",
            config=dict(
                model="gemini-1.5-flash",
            ),
        ),
        embedder=dict(
            provider="google",
            config=dict(
                model="models/embedding-001",  
                task_type="retrieval_document",
            ),
        ),
    )
)

# TXT Search Tool
job_desc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "devops_job_desc.txt"))
txt_search_tool = TXTSearchTool(
    txt=job_desc_path,
    config=dict(
        llm=dict(
            provider="google",
            config=dict(
                model="gemini-1.5-flash",
            ),
        ),
        embedder=dict(
            provider="google",
            config=dict(
                model="models/embedding-001",  
                task_type="retrieval_document",
            ),
        ),
    )
)


# Setting up the agents

# Job Description Analyst
jd_agent = Agent(
    role="Job Description Analyst",
    goal="Thoroughly analyze job descriptions to extract technical skills, soft skills, qualifications, and key responsibilities",
    backstory="Specialized in parsing complex job descriptions across industries to identify core requirements and hidden expectations",
    tools=[txt_search_tool],
    llm=llm,
    verbose=True,
    memory=True,
    instructions="""
    1. Carefully read the entire job description
    2. Identify and categorize:
       - Must-have technical skills (programming languages, tools, methodologies)
       - Preferred qualifications
       - Soft skills and personality traits
       - Years of experience required
       - Education/certification requirements
       - Key responsibilities and deliverables
    3. Highlight any ambiguous terms that need clarification
    4. Output in structured format with clear prioritization
    """
)

# Resume-JD Gap Analyst
gap_agent = Agent(
    role="Resume-JD Gap Analyst",
    goal="Systematically compare resume content with job requirements to identify missing and weak areas",
    backstory="Expert in ATS systems and hiring manager psychology, knows what makes resumes get rejected",
    tools=[pdf_search_tool, txt_search_tool],
    llm=llm,
    memory=True,
    verbose=True,
    instructions="""
    1. Perform side-by-side analysis of resume vs. job description
    2. Identify:
       - Missing hard skills that are required
       - Missing soft skills that are emphasized
       - Experience gaps (years, types of roles)
       - Underrepresented qualifications
       - Potential red flags in resume
    3. Categorize gaps by severity (critical vs. nice-to-have)
    4. Note any transferable skills that could compensate
    5. Provide specific improvement recommendations
    """
)

# Resume Optimization Coach
rag_agent = Agent(
    role="Resume Optimization Coach",
    goal="Provide data-driven suggestions for resume improvement using industry best practices",
    backstory="Trained on thousands of successful resumes and hiring trends across industries",
    llm=llm,
    memory=True,
    verbose=True,
    tools=[pdf_search_tool],
    instructions="""
    1. Apply proven resume writing principles:
       - STAR (Situation, Task, Action, Result) method
       - Quantifiable achievements
       - Action verb usage
       - ATS optimization techniques
    2. Suggest industry-specific phrasing
    3. Recommend optimal:
       - Section ordering
       - Bullet point structure
       - Keyword density
       - Technical skill presentation
    4. Provide before/after examples for problematic sections
    """
)

# Resume Transformation Specialist
enhancer_agent = Agent(
    role="Resume Transformation Specialist",
    goal="Rewrite resume content to closely align with job requirements while maintaining authenticity",
    backstory="Expert linguist and former recruiter who understands how to tailor resumes effectively",
    llm=llm,
    memory=True,
    verbose=True,
    instructions="""
    1. Synthesize inputs from JD analysis, gap analysis, and RAG suggestions
    2. Rewrite resume sections to:
       - Incorporate missing keywords naturally
       - Highlight most relevant experiences first
       - Strengthen weak areas without misrepresentation
       - Optimize for both ATS and human readers
    3. Maintain original meaning while enhancing impact
    4. Provide version control showing changes made
    5. Explain rationale for key modifications
    """
)

# Setting up the tasks
task1 = Task(
    name="Comprehensive Job Description Breakdown",
    description="""
    Conduct a thorough analysis of the provided job description to create a detailed requirements profile.
    Output should include:
    1. Categorized technical skills (with priority ranking)
    2. Explicit and implicit soft skills sought
    3. Education/credential requirements
    4. Experience requirements (years, types)
    5. Key responsibilities (daily tasks and deliverables)
    6. Any industry-specific terminology or jargon
    7. Company culture indicators
    8. Potential red flags in the description
    """,
    expected_output="Structured table with categorized requirements and priority indicators",
    agent=jd_agent,
    output_file="jd_analysis.json",
    tools=[txt_search_tool]
)

task2 = Task(
    name="Resume-JD Gap Analysis Report",
    description="""
    Perform a detailed gap analysis between the candidate's resume and job requirements.
    Identify:
    1. Exact skill matches (highlight strengths)
    2. Missing critical skills (with severity rating)
    3. Partial matches that need strengthening
    4. Experience gaps (duration, role types)
    5. Potential transferable skills
    6. Formatting/content issues hurting ATS score
    7. Opportunities to better showcase relevant experience
    
    Provide specific examples from both documents.
    """,
    expected_output="Detailed gap report with side-by-side comparisons and improvement roadmap",
    agent=gap_agent,
    output_file="gap_analysis.json",
    tools=[pdf_search_tool, txt_search_tool]
)

task3 = Task(
    name="Resume Optimization Strategy",
    description="""
    Generate actionable resume improvement recommendations based on:
    1. Current industry hiring trends for this role
    2. ATS optimization best practices
    3. Effective achievement articulation
    4. Proper keyword incorporation
    5. Visual hierarchy improvements
    
    Include specific before/after examples for the candidate's resume.
    """,
    expected_output="List of prioritized recommendations with concrete examples",
    output_file="rag_analysis.json",
    agent=rag_agent,
    tools=[pdf_search_tool]
)

task4 = Task(
    name="Resume Transformation",
    description="""
    Create an enhanced version of the resume that:
    1. Addresses all critical gaps from the analysis
    2. Naturally incorporates required keywords
    3. Highlights most relevant qualifications
    4. Maintains authenticity and truthfulness
    5. Optimizes for both ATS and human readers
    
    Provide:
    - Full revised resume
    - Change log explaining modifications
    - Version comparison highlighting improvements
    """,
    expected_output="Polished resume version with documentation of changes made",
    output_file="enhancement_analysis.json",   
    agent=enhancer_agent,
    tools=[pdf_search_tool, txt_search_tool]
)

# Setting up the crew
crew = Crew(
    agents=[jd_agent, gap_agent, rag_agent, enhancer_agent],
    tasks=[task1, task2, task3, task4],
    process=Process.sequential,
)

crew.kickoff()