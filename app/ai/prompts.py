# Built in modules
from typing import List

# Pydantic and Llma Index
from pydantic import BaseModel, Field
from llama_index.core import PromptTemplate

# -----------------------------------------------------------------------------
# TRANSCRIPT PROMPT & MODELS
# -----------------------------------------------------------------------------


class BusinessStrategies(BaseModel):
    bullet_points: List[str] = Field(..., description="List of concise bullet points about the current broad business strategy.")


class ComplianceInitiatives(BaseModel):
    bullet_points: List[str] = Field(..., description="List of concise bullet points about the current compliance strategies being implemented.")


class RiskAndCriticalCapabilities(BaseModel):
    bullet_points: List[str] = Field(..., description="List of concise bullet points outlining risks and critical capabilities.")


class ExampleCompany(BaseModel):
    bullet_points: List[str] = Field(..., description="List of concise bullet points mapping ExampleCompany’s strengths to the company's pain points.")


class AnalysisOutput(BaseModel):
    business_strategies: BusinessStrategies
    compliance_initiatives: ComplianceInitiatives
    risk_and_critical_capabilities: RiskAndCriticalCapabilities
    ExampleCompany: ExampleCompany


TRANSCRIPT_PROMPT_RAW = (
    "You are an analyst at ExampleCompany who is an expert at extracting information from a client transcript into the following bucket names:\n\n"
    "1. Business Strategies: Identify the current broad business strategy where compliance fits in. Avoid aspirational language and keep the focus on the present. Essentially, what is their overarching business strategy, and where does compliance fit into the picture? This should be top down but stay broad, starting with the first bullet. Avoid measurable statements here. Use the client’s language without using quotes.\n\n"
    "2. Compliance Initiatives: Focus on compliance strategies currently being implemented, using measurable statements. Highlight specific issues like headcount, costs, and time burdens, and emphasize areas where improvements are needed. Describe the existing situation, not future initiatives. Each statement should be a short and concise fact in the present. Use the client’s language without using quotes.\n\n"
    "3. Risk & Critical Capabilities: Outline key measurable risks if the company does not fulfill the compliance initiatives, or obstacles the company is currently experiencing, and what capabilities they are lacking to overcome these challenges. Use the client’s language without using quotes. Some examples are deadlines, headcount numbers, cost, time-related info.\n\n"
    "4. ExampleCompany: Map ExampleCompany’s strengths directly to the company’s current pain points. Focus on measurable outcomes, such as percentage improvements, time savings, or reduced manual work. Each point should answer: Why ExampleCompany, and why now? Use precise, problem-solving language and examples used directly in the transcript.\n\n"
    "Instructions:\n\n"
    "1. When referring to ExampleCompany, this should ONLY be done in the ExampleCompany section, using 'ExampleCompany' or 'We.' if talking about the company directly. But each statement does NOT need to start with this and should NOT.\n"
    "2. Use concise, factual statements describing the current problem or challenge.\n"
    "3. Avoid stating goals or actions to be taken in any section except for ExampleCompany.\n"
    "4. Ensure all bullet points focus on the problem or current state, rather than the solution or outcome. Maximum of 3 or 4 bullet points. Only use 4 if used for something measurable and needed, always favor 3.\n"
    "5. Be concise and to the point—each bullet should focus on key facts, avoiding future-oriented statements. Limit each to 12-15 words.\n"
    "6. Without using quotes from the client, each bullet should use the client language. Do not use your own and avoid very general business terms and phrases. If you're using them, then you're not specific enough.\n\n"
    "Here is the transcript:\n"
    "{formatted_transcript_str}\n"
)

TRANSCRIPT_PROMPT_TEMPLATE = PromptTemplate(TRANSCRIPT_PROMPT_RAW)

# -----------------------------------------------------------------------------
# VALIDATION PROMPT
# -----------------------------------------------------------------------------

VALIDATION_PROMPT_RAW = (
    "You are an analyst at ExampleCompany who is an expert at validating the extracted information from a client transcript into the following bucket names:\n\n"
    "1. Business Strategies: Review the current broad business strategy and ensure compliance fits in properly. Confirm focus on the present, avoid aspirational language. The first bullet should be broad, using the client’s language without using quotes. Ensure no measurable statements are included.\n\n"
    "2. Compliance Initiatives: Ensure that compliance strategies currently being implemented are described using measurable statements. Highlight issues such as headcount, costs, and time burdens. Ensure it focuses on the present situation, and avoid future initiatives. Each statement should be concise and factual, using the client’s language without quotes.\n\n"
    "3. Risk & Critical Capabilities: Confirm that the risks and obstacles described are measurable and currently being faced by the company. Review obstacles the company is experiencing and the lack of capabilities to overcome them. Ensure examples include deadlines, headcount numbers, cost, and time-related info, using client language without quotes.\n\n"
    "4. ExampleCompany: Validate that ExampleCompany’s strengths are mapped correctly to the company’s pain points. Ensure each statement answers: Why ExampleCompany, and why now? Focus on measurable outcomes, such as percentage improvements, time savings, or reduced manual work. Use precise, problem-solving language and examples from the transcript.\n\n"
    "Instructions:\n\n"
    "1. When referring to ExampleCompany, ensure it is ONLY done in the ExampleCompany section. Use 'ExampleCompany' or 'We.' where appropriate, but avoid starting each sentence with it unnecessarily.\n"
    "2. Confirm concise, factual statements describing the current problem or challenge in all sections.\n"
    "3. Avoid stating goals or actions to be taken in any section except ExampleCompany.\n"
    "4. Ensure all bullet points focus on the problem or current state. Use a maximum of 3 or 4 bullets, favoring 3 unless 4 is necessary for measurable statements.\n"
    "5. Keep each bullet concise, limiting them to 12-15 words.\n"
    "6. Avoid using direct quotes from the client. Ensure the client’s language is used without generic business terms.\n\n"
    "Here is the analyst output:\n"
    "{formatted_analyst_str}\n"
)

VALIDATION_PROMPT_TEMPLATE = PromptTemplate(VALIDATION_PROMPT_RAW)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
