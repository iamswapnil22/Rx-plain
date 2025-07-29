"""
Medical Prompt Templates and Safety Guidelines for Rxplain
Comprehensive medical assistant prompts and safety protocols
"""

# Medical Safety Guidelines
MEDICAL_SAFETY_GUIDELINES = {
    "never_do": [
        "Provide medical diagnoses",
        "Recommend specific treatments or dosages",
        "Replace professional medical advice",
        "Make treatment decisions",
        "Prescribe medications",
        "Interpret medical test results",
        "Provide emergency medical advice"
    ],
    "always_do": [
        "Encourage consulting healthcare professionals",
        "Include safety warnings when appropriate",
        "Use clear, accessible language",
        "Provide educational information only",
        "Emphasize the importance of professional medical care",
        "Include relevant disclaimers"
    ]
}

# Medical Query Categories
MEDICAL_QUERY_CATEGORIES = {
    "medication": {
        "keywords": [
            "medication", "medicine", "drug", "pill", "tablet", "capsule", "injection",
            "prescription", "dosage", "side effect", "interaction", "allergy",
            "metformin", "aspirin", "ibuprofen", "acetaminophen", "antibiotic",
            "blood pressure", "diabetes", "cholesterol", "pain", "fever"
        ],
        "template": """
**Medication Information: {medication_name}**

**What is it?**
{brief_description}

**What is it used for?**
{primary_uses}

**How does it work?**
{mechanism_explanation}

**Common side effects:**
{side_effects_list}

**Important precautions:**
{precautions_list}

**When to contact your doctor:**
{warning_signs}

**Additional tips:**
{additional_info}

⚠️ **Important**: This information is for educational purposes only and should not replace professional medical advice. Always consult your healthcare provider for personalized medical guidance.
"""
    },
    "symptom": {
        "keywords": [
            "symptom", "pain", "fever", "headache", "nausea", "dizziness", "fatigue",
            "cough", "sore throat", "rash", "swelling", "bleeding", "chest pain",
            "shortness of breath", "abdominal pain", "back pain"
        ],
        "template": """
**Symptom Information: {symptom_name}**

**What it might mean:**
{possible_causes}

**When to be concerned:**
{red_flags}

**Self-care tips:**
{safe_remedies}

**When to see a doctor:**
{medical_attention_needed}

⚠️ **Important**: This information is for educational purposes only. If you're experiencing severe symptoms, seek immediate medical attention.
"""
    },
    "general_health": {
        "keywords": [
            "health", "wellness", "nutrition", "exercise", "sleep", "stress",
            "prevention", "lifestyle", "diet", "fitness", "mental health"
        ],
        "template": """
**Health Information: {topic}**

**Overview:**
{general_info}

**Key points:**
{key_points}

**Important considerations:**
{safety_info}

**When to seek medical help:**
{warning_signs}

⚠️ **Important**: This information is for educational purposes only. Consult your healthcare provider for personalized advice.
"""
    }
}

# Safety Warning Templates
SAFETY_WARNINGS = {
    "side_effects": "⚠️ **Safety Alert**: If you experience severe side effects, allergic reactions, or unusual symptoms, seek immediate medical attention.",
    "dosage": "⚠️ **Dosage Warning**: Always follow your healthcare provider's prescribed dosage. Never adjust medication doses without consulting your doctor.",
    "interactions": "⚠️ **Interaction Warning**: Always inform your healthcare provider about all medications, supplements, and substances you're taking to avoid harmful interactions.",
    "pregnancy": "⚠️ **Pregnancy/Breastfeeding**: Consult your healthcare provider before taking any medication during pregnancy or while breastfeeding.",
    "discontinuation": "⚠️ **Discontinuation Warning**: Never stop taking prescribed medications without consulting your healthcare provider, as this can be dangerous.",
    "emergency": "🚨 **EMERGENCY**: If you're experiencing a medical emergency, call emergency services immediately. Do not rely on AI assistants for emergency medical care."
}

# Medical Response Templates
MEDICAL_RESPONSE_TEMPLATES = {
    "medication_query": {
        "structure": [
            "Medication overview",
            "Uses and indications", 
            "How it works (simplified)",
            "Common side effects",
            "Important precautions",
            "When to contact healthcare provider",
            "Additional helpful tips"
        ],
        "formatting": {
            "use_bullet_points": True,
            "use_bold_warnings": True,
            "include_disclaimer": True,
            "max_length": 1000
        }
    },
    "symptom_query": {
        "structure": [
            "Possible causes",
            "Red flags and warning signs",
            "Safe home remedies",
            "When to seek medical attention"
        ],
        "formatting": {
            "use_bullet_points": True,
            "use_bold_warnings": True,
            "include_disclaimer": True,
            "max_length": 800
        }
    },
    "general_health_query": {
        "structure": [
            "General information",
            "Key points",
            "Safety considerations",
            "Professional consultation guidance"
        ],
        "formatting": {
            "use_bullet_points": True,
            "use_bold_warnings": False,
            "include_disclaimer": True,
            "max_length": 600
        }
    }
}

# Medical Disclaimer Templates
MEDICAL_DISCLAIMERS = {
    "standard": "⚠️ **Important**: This information is for educational purposes only and should not replace professional medical advice. Always consult your healthcare provider for personalized medical guidance.",
    "emergency": "🚨 **EMERGENCY DISCLAIMER**: If you're experiencing a medical emergency, call emergency services immediately. This AI assistant cannot provide emergency medical care.",
    "medication": "⚠️ **Medication Disclaimer**: This information is for educational purposes only. Always follow your healthcare provider's instructions and never adjust medications without consulting them.",
    "symptom": "⚠️ **Symptom Disclaimer**: This information is for educational purposes only. If you're experiencing concerning symptoms, seek professional medical evaluation."
}

# Medical Keywords for Query Classification
MEDICAL_KEYWORDS = {
    "medications": [
        "medication", "medicine", "drug", "pill", "tablet", "capsule", "injection",
        "prescription", "dosage", "side effect", "interaction", "allergy",
        "metformin", "aspirin", "ibuprofen", "acetaminophen", "antibiotic",
        "blood pressure", "diabetes", "cholesterol", "pain", "fever"
    ],
    "symptoms": [
        "symptom", "pain", "fever", "headache", "nausea", "dizziness", "fatigue",
        "cough", "sore throat", "rash", "swelling", "bleeding", "chest pain",
        "shortness of breath", "abdominal pain", "back pain"
    ],
    "conditions": [
        "diabetes", "hypertension", "heart disease", "asthma", "arthritis",
        "depression", "anxiety", "cancer", "stroke", "kidney disease"
    ],
    "emergency": [
        "emergency", "urgent", "immediate", "severe", "serious", "dangerous",
        "chest pain", "difficulty breathing", "unconscious", "seizure"
    ]
}

def classify_medical_query(query: str) -> str:
    """
    Classify a medical query into categories
    """
    query_lower = query.lower()
    
    # Check for emergency keywords first
    if any(keyword in query_lower for keyword in MEDICAL_KEYWORDS["emergency"]):
        return "emergency"
    
    # Check for medication keywords
    if any(keyword in query_lower for keyword in MEDICAL_KEYWORDS["medications"]):
        return "medication"
    
    # Check for symptom keywords
    if any(keyword in query_lower for keyword in MEDICAL_KEYWORDS["symptoms"]):
        return "symptom"
    
    # Check for condition keywords
    if any(keyword in query_lower for keyword in MEDICAL_KEYWORDS["conditions"]):
        return "condition"
    
    # Default to general health
    return "general_health"

def get_appropriate_disclaimer(query_type: str) -> str:
    """
    Get appropriate disclaimer based on query type
    """
    if query_type == "emergency":
        return MEDICAL_DISCLAIMERS["emergency"]
    elif query_type == "medication":
        return MEDICAL_DISCLAIMERS["medication"]
    elif query_type == "symptom":
        return MEDICAL_DISCLAIMERS["symptom"]
    else:
        return MEDICAL_DISCLAIMERS["standard"]

def get_safety_warnings(query: str) -> list:
    """
    Get appropriate safety warnings based on query content
    """
    warnings = []
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["side effect", "reaction", "allergy"]):
        warnings.append(SAFETY_WARNINGS["side_effects"])
    
    if any(word in query_lower for word in ["dosage", "dose", "how much", "frequency"]):
        warnings.append(SAFETY_WARNINGS["dosage"])
    
    if any(word in query_lower for word in ["interaction", "mix", "combine", "alcohol"]):
        warnings.append(SAFETY_WARNINGS["interactions"])
    
    if any(word in query_lower for word in ["pregnancy", "breastfeeding", "baby"]):
        warnings.append(SAFETY_WARNINGS["pregnancy"])
    
    if any(word in query_lower for word in ["stop", "discontinue", "quit"]):
        warnings.append(SAFETY_WARNINGS["discontinuation"])
    
    if any(word in query_lower for word in ["emergency", "urgent", "immediate", "severe"]):
        warnings.append(SAFETY_WARNINGS["emergency"])
    
    return warnings

def format_medical_response(response: str, query_type: str, warnings: list = None) -> str:
    """
    Format medical response with appropriate warnings and disclaimers
    """
    formatted_response = response
    
    # Add warnings at the beginning if any
    if warnings:
        formatted_response = "\n\n".join(warnings) + "\n\n" + formatted_response
    
    # Add appropriate disclaimer
    disclaimer = get_appropriate_disclaimer(query_type)
    if disclaimer not in formatted_response:
        formatted_response += f"\n\n{disclaimer}"
    
    return formatted_response 