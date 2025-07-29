import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import HTTPException, status
import json
import base64
from typing import Optional, Union
from PIL import Image
import io

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Comprehensive Medical Assistant System Prompt
MEDICAL_SYSTEM_PROMPT = """You are Rxplain, a professional medical AI assistant designed to help patients understand their medications and health information. Your role is to provide clear, accurate, and helpful medical information while maintaining the highest standards of safety and ethics.

## CORE RESPONSIBILITIES:
1. **Medication Information**: Explain drug names, uses, dosages, side effects, and interactions
2. **Health Education**: Provide general health information and wellness advice
3. **Safety Guidance**: Always emphasize when to consult healthcare professionals
4. **Patient Support**: Help patients understand their treatment plans
5. **Image Analysis**: Analyze prescription images and medical documents (when provided)

## SAFETY GUIDELINES:
- **NEVER provide medical diagnoses**
- **NEVER recommend specific treatments or dosages**
- **ALWAYS encourage consulting healthcare professionals for medical decisions**
- **ALWAYS include safety warnings when appropriate**
- **NEVER replace professional medical advice**
- **For image analysis**: Only provide educational information, never diagnostic interpretations

## RESPONSE STRUCTURE:
Your responses should be:
1. **Clear and Accessible**: Use simple, non-technical language
2. **Comprehensive**: Cover key aspects like uses, side effects, precautions
3. **Safety-Focused**: Include relevant warnings and when to seek medical help
4. **Educational**: Help patients understand their medications better
5. **Professional**: Maintain a caring but professional tone

## FORMATTING GUIDELINES:
- Use bullet points for lists
- Use bold text for important warnings
- Use clear headings for different sections
- Keep paragraphs short and readable
- Include relevant medical symbols when appropriate (e.g., ⚠️ for warnings)

## MEDICAL DISCLAIMER:
Always include this disclaimer when providing medication information:
"⚠️ **Important**: This information is for educational purposes only and should not replace professional medical advice. Always consult your healthcare provider for personalized medical guidance."

## IMAGE ANALYSIS GUIDELINES:
When analyzing prescription images:
1. **Identify medications** clearly and accurately
2. **Explain each medication's purpose** in simple terms
3. **List common side effects** for each medication
4. **Highlight potential interactions** between medications
5. **Provide dosage information** (general, not specific to patient)
6. **Include storage and timing advice**
7. **Emphasize the importance of following healthcare provider instructions**

## RESPONSE TEMPLATE:
For medication queries, structure your response as:
1. **What is [medication]?** - Brief overview
2. **What is it used for?** - Primary and common uses
3. **How does it work?** - Simple mechanism explanation
4. **Common side effects** - Most frequent side effects
5. **Important precautions** - Safety information
6. **When to contact your doctor** - Red flags and concerns
7. **Additional tips** - Storage, timing, lifestyle considerations

Remember: You are a supportive medical assistant, not a replacement for professional healthcare."""

# Prescription Image Analysis Prompt
PRESCRIPTION_IMAGE_PROMPT = """You are analyzing a prescription image. Please provide a comprehensive analysis of the medications shown:

**ANALYSIS REQUIREMENTS:**
1. **Identify each medication** by name and type
2. **Explain the purpose** of each medication in simple terms
3. **List common side effects** for each medication
4. **Highlight potential interactions** between the medications
5. **Provide general dosage information** (not specific to patient)
6. **Include storage and administration tips**
7. **Emphasize the importance of following healthcare provider instructions**

**RESPONSE FORMAT:**
Structure your response as:

**Prescription Analysis:**
[Overall summary of the prescription]

**Medications Identified:**
1. **[Medication Name]**
   - **Purpose**: [What it's used for]
   - **How it works**: [Simple explanation]
   - **Common side effects**: [List side effects]
   - **Important precautions**: [Safety information]

2. **[Next Medication Name]**
   [Same structure as above]

**Potential Interactions:**
[List any interactions between the medications]

**General Guidelines:**
- [Storage instructions]
- [Timing recommendations]
- [Lifestyle considerations]

**When to Contact Your Doctor:**
[List warning signs and red flags]

⚠️ **Important**: This analysis is for educational purposes only. Always follow your healthcare provider's specific instructions and consult them for personalized medical guidance."""

# Safety filters and medical keywords
MEDICAL_SAFETY_FILTERS = [
    "emergency", "urgent", "immediate", "severe", "serious", "dangerous",
    "overdose", "allergic", "reaction", "chest pain", "difficulty breathing",
    "swelling", "rash", "fever", "bleeding", "dizziness", "fainting"
]

def create_medical_prompt(user_query: str, has_image: bool = False) -> str:
    """
    Create a comprehensive medical prompt with safety guidelines
    """
    # Detect if this is a medication-related query
    medication_keywords = [
        "medication", "medicine", "drug", "pill", "tablet", "capsule", "injection",
        "prescription", "dosage", "side effect", "interaction", "allergy",
        "metformin", "aspirin", "ibuprofen", "acetaminophen", "antibiotic",
        "blood pressure", "diabetes", "cholesterol", "pain", "fever"
    ]
    
    is_medication_query = any(keyword.lower() in user_query.lower() for keyword in medication_keywords)
    
    # Enhanced prompt based on query type and image presence
    if has_image:
        if is_medication_query or "prescription" in user_query.lower():
            enhanced_prompt = f"""
{MEDICAL_SYSTEM_PROMPT}

{PRESCRIPTION_IMAGE_PROMPT}

**USER QUERY**: {user_query}

**INSTRUCTIONS**: 
- Analyze the prescription image provided
- Identify all medications clearly
- Provide comprehensive information about each medication
- Include safety warnings and precautions
- Explain in simple, patient-friendly language
- Always emphasize consulting healthcare professionals
- Structure the response clearly with headings

**RESPONSE FORMAT**:
Please provide a well-structured response covering:
1. Overall prescription summary
2. Each medication identified with detailed information
3. Potential interactions between medications
4. General guidelines for storage and administration
5. When to contact healthcare provider
6. Additional helpful tips

Remember to maintain a caring, professional tone and prioritize patient safety.
"""
        else:
            enhanced_prompt = f"""
{MEDICAL_SYSTEM_PROMPT}

**USER QUERY**: {user_query}

**INSTRUCTIONS**:
- Analyze the medical image provided
- Provide helpful health information
- Maintain medical accuracy
- Use clear, accessible language
- Include relevant safety information
- Encourage professional consultation when appropriate
- NEVER provide diagnostic interpretations

**RESPONSE FORMAT**:
Provide a clear, informative response that:
- Addresses the user's question about the image
- Includes relevant health information
- Maintains safety guidelines
- Uses appropriate medical terminology
- Encourages professional consultation when needed
"""
    elif is_medication_query:
        enhanced_prompt = f"""
{MEDICAL_SYSTEM_PROMPT}

**USER QUERY**: {user_query}

**INSTRUCTIONS**: 
- Provide comprehensive medication information
- Include safety warnings and precautions
- Explain in simple, patient-friendly language
- Always emphasize consulting healthcare professionals
- Structure the response clearly with headings

**RESPONSE FORMAT**:
Please provide a well-structured response covering:
1. Medication overview
2. Uses and indications
3. How it works (simplified)
4. Common side effects
5. Important precautions
6. When to contact healthcare provider
7. Additional helpful tips

Remember to maintain a caring, professional tone and prioritize patient safety.
"""
    else:
        enhanced_prompt = f"""
{MEDICAL_SYSTEM_PROMPT}

**USER QUERY**: {user_query}

**INSTRUCTIONS**:
- Provide helpful health information
- Maintain medical accuracy
- Use clear, accessible language
- Include relevant safety information
- Encourage professional consultation when appropriate

**RESPONSE FORMAT**:
Provide a clear, informative response that:
- Addresses the user's question directly
- Includes relevant health information
- Maintains safety guidelines
- Uses appropriate medical terminology
- Encourages professional consultation when needed
"""

    return enhanced_prompt

def add_safety_warnings(response: str, user_query: str, has_image: bool = False) -> str:
    """
    Add appropriate safety warnings based on the query content
    """
    query_lower = user_query.lower()
    
    # Add specific warnings based on query content
    warnings = []
    
    if has_image:
        warnings.append("⚠️ **Image Analysis Disclaimer**: This analysis is for educational purposes only. Always consult your healthcare provider for accurate medical information and follow their specific instructions.")
    
    if any(word in query_lower for word in ["side effect", "reaction", "allergy"]):
        warnings.append("⚠️ **Safety Alert**: If you experience severe side effects, allergic reactions, or unusual symptoms, seek immediate medical attention.")
    
    if any(word in query_lower for word in ["dosage", "dose", "how much", "frequency"]):
        warnings.append("⚠️ **Dosage Warning**: Always follow your healthcare provider's prescribed dosage. Never adjust medication doses without consulting your doctor.")
    
    if any(word in query_lower for word in ["interaction", "mix", "combine", "alcohol"]):
        warnings.append("⚠️ **Interaction Warning**: Always inform your healthcare provider about all medications, supplements, and substances you're taking to avoid harmful interactions.")
    
    if any(word in query_lower for word in ["pregnancy", "breastfeeding", "baby"]):
        warnings.append("⚠️ **Pregnancy/Breastfeeding**: Consult your healthcare provider before taking any medication during pregnancy or while breastfeeding.")
    
    if any(word in query_lower for word in ["stop", "discontinue", "quit"]):
        warnings.append("⚠️ **Discontinuation Warning**: Never stop taking prescribed medications without consulting your healthcare provider, as this can be dangerous.")
    
    # Add general medical disclaimer if not already present
    if "⚠️ **Important**:" not in response:
        response += "\n\n⚠️ **Important**: This information is for educational purposes only and should not replace professional medical advice. Always consult your healthcare provider for personalized medical guidance."
    
    # Add specific warnings at the beginning if any were identified
    if warnings:
        response = "\n\n".join(warnings) + "\n\n" + response
    
    return response

async def query_gemini(prompt: str, image_data: Optional[bytes] = None) -> str:
    """
    Enhanced Gemini query function with medical assistant capabilities and image support
    """
    try:
        # Create comprehensive medical prompt
        has_image = image_data is not None
        medical_prompt = create_medical_prompt(prompt, has_image)
        
        # Prepare content for Gemini
        if image_data:
            # Convert image data to PIL Image and then to format Gemini can handle
            try:
                image = Image.open(io.BytesIO(image_data))
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Generate response with image
                response = model.generate_content([medical_prompt, image])
            except Exception as img_error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error processing image: {str(img_error)}"
                )
        else:
            # Generate response with text only
            response = model.generate_content(medical_prompt)
        
        if not response.text:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Empty response from Gemini"
            )
        
        # Add safety warnings based on query content
        enhanced_response = add_safety_warnings(response.text, prompt, has_image)
        
        return enhanced_response
        
    except Exception as e:
        # Provide a helpful error message for medical queries
        error_message = f"Gemini API error: {str(e)}"
        
        # If it's a medical query, provide a more helpful response
        if any(keyword in prompt.lower() for keyword in ["medication", "medicine", "drug", "health", "symptom", "prescription"]):
            return """I apologize, but I'm currently experiencing technical difficulties. 

For medical questions, please:
1. **Contact your healthcare provider** for immediate medical advice
2. **Visit reliable medical websites** like Mayo Clinic, WebMD, or MedlinePlus
3. **Call emergency services** if you're experiencing a medical emergency

⚠️ **Important**: Never delay seeking professional medical help due to technical issues with AI assistants.

Your health and safety are the top priority."""
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_message
        )

# Additional utility functions for medical assistance
def validate_medical_query(query: str) -> bool:
    """
    Validate if a query is medical-related
    """
    medical_keywords = [
        "medication", "medicine", "drug", "health", "symptom", "treatment",
        "side effect", "dosage", "prescription", "doctor", "nurse", "hospital",
        "pain", "fever", "allergy", "reaction", "blood", "heart", "diabetes",
        "blood pressure", "cholesterol", "antibiotic", "vitamin", "supplement"
    ]
    
    return any(keyword.lower() in query.lower() for keyword in medical_keywords)

def get_medical_response_template(query_type: str) -> str:
    """
    Get appropriate response template based on query type
    """
    templates = {
        "medication": """
**Medication Information: [MEDICATION NAME]**

**What is it?**
[Brief description]

**What is it used for?**
[Primary uses and indications]

**How does it work?**
[Simple explanation of mechanism]

**Common side effects:**
• [Side effect 1]
• [Side effect 2]
• [Side effect 3]

**Important precautions:**
• [Precaution 1]
• [Precaution 2]

**When to contact your doctor:**
• [Warning sign 1]
• [Warning sign 2]

**Additional tips:**
[Helpful information about storage, timing, etc.]
""",
        "prescription_image": """
**Prescription Analysis:**

**Medications Identified:**
1. **[Medication Name]**
   - **Purpose**: [What it's used for]
   - **How it works**: [Simple explanation]
   - **Common side effects**: [List side effects]
   - **Important precautions**: [Safety information]

2. **[Next Medication Name]**
   [Same structure as above]

**Potential Interactions:**
[List any interactions between the medications]

**General Guidelines:**
- [Storage instructions]
- [Timing recommendations]
- [Lifestyle considerations]

**When to Contact Your Doctor:**
[List warning signs and red flags]
""",
        "general_health": """
**Health Information: [TOPIC]**

**Overview:**
[General information]

**Key points:**
• [Point 1]
• [Point 2]
• [Point 3]

**Important considerations:**
[Safety and precaution information]

**When to seek medical help:**
[Warning signs and red flags]
""",
        "symptom": """
**Symptom Information: [SYMPTOM]**

**What it might mean:**
[Possible causes]

**When to be concerned:**
[Red flags and warning signs]

**Self-care tips:**
[Safe home remedies and lifestyle changes]

**When to see a doctor:**
[Specific situations requiring medical attention]
"""
    }
    
    return templates.get(query_type, templates["general_health"])
