"""
Excel Data -> AI Prompt (step 2 of the pipeline).

Turns a structured Lead (Name, Service, Budget, City) into the prompt the AI
calling agent actually uses on the call: a system prompt with full context,
an opening line personalised with the lead's name/service/city, and a set of
relevant follow-up questions instead of one generic script for every lead.
"""

from __future__ import annotations

from .schemas import AIPromptPreview, Lead

# Service-specific qualifying questions. Falls back to GENERIC_QUESTIONS
# when the lead's service does not match a known key (substring match).
SERVICE_QUESTIONS: dict[str, list[str]] = {
    "website development": [
        "Do you already have a domain and hosting, or should we include that?",
        "Is this a new website or a redesign of an existing one?",
        "How many pages or key sections do you expect (Home, About, Services, etc.)?",
        "Do you need e-commerce / online payment functionality?",
        "What's your ideal timeline to go live?",
    ],
    "mobile app development": [
        "Is this for Android, iOS, or both?",
        "Do you have wireframes or a reference app in mind?",
        "Will the app need a backend/admin panel as well?",
        "What's your target launch timeline?",
    ],
    "digital marketing": [
        "Which platforms are you most interested in — Google, Meta, or both?",
        "Do you have past campaign data we can review?",
        "What's the primary goal — leads, sales, or brand awareness?",
    ],
    "seo": [
        "Do you have an existing website that needs ranking improvement?",
        "Which keywords or locations matter most to your business?",
        "Have you worked with an SEO agency before?",
    ],
    "esign": [
        "Roughly how many documents do you send for signature each month?",
        "Do you need Aadhaar eSign, DSC-based signing, or both?",
        "Will this integrate with an existing CRM or document system?",
    ],
}

GENERIC_QUESTIONS = [
    "What exactly are you looking to achieve with this service?",
    "Do you have a budget range and timeline in mind?",
    "Have you already spoken to other vendors for this?",
]


def _questions_for_service(service: str | None) -> list[str]:
    if not service:
        return GENERIC_QUESTIONS
    service_key = service.strip().lower()
    for key, questions in SERVICE_QUESTIONS.items():
        if key in service_key or service_key in key:
            return questions
    return GENERIC_QUESTIONS


def build_prompt(lead: Lead) -> AIPromptPreview:
    """Build the structured AI prompt for a single lead.

    This is what turns a plain Excel row into relevant, lead-specific
    questions instead of the same generic script for every call.
    """

    service = lead.service or "our services"
    city = f" in {lead.city}" if lead.city else ""
    budget_line = f" They mentioned a budget of {lead.budget}." if lead.budget else ""

    context = {
        "lead_name": lead.name,
        "service": lead.service,
        "budget": lead.budget,
        "location": lead.city,
    }

    system_prompt = (
        "You are a polite, professional sales representative for Sofzenix making an "
        f"outbound call to {lead.name}, a lead who enquired about {service}{city}."
        f"{budget_line} Speak naturally, listen actively, do not read questions "
        "verbatim like a script, and adapt based on the lead's responses. "
        "Your goal is to qualify interest, answer basic questions, and either "
        "book a follow-up call, schedule an appointment, or politely close the "
        "lead if they are not interested."
    )

    opening_line = (
        f"Hi {lead.name}, this is calling from Sofzenix regarding your enquiry "
        f"for {service}{city}. Do you have a couple of minutes to talk?"
    )

    return AIPromptPreview(
        lead_id=lead.id,
        system_prompt=system_prompt,
        opening_line=opening_line,
        key_questions=_questions_for_service(lead.service),
        context=context,
    )
