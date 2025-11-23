"""Sample synthetic clinical notes for testing and demonstration."""

SAMPLE_NOTES = {
    "chest_pain": """Patient is a 45-year-old male presenting with complaint of chest discomfort for 2 days. Patient reports the pain as pressure-like, rated 6/10, occurring with exertion. Patient denies shortness of breath, nausea, or diaphoresis. History of hypertension, currently on Lisinopril 10mg daily. Patient denies smoking but reports occasional alcohol use. 

Vital signs: BP 142/88 mmHg, HR 78 bpm, Temp 98.6°F, RR 16, O2 sat 98% on room air.

Physical examination reveals patient is alert and oriented. Heart sounds regular without murmurs. Lungs clear to auscultation bilaterally. No peripheral edema noted.

Assessment: Atypical chest pain, likely musculoskeletal given characteristics. Rule out cardiac etiology given risk factors.

Plan: Order ECG and troponin levels. Start patient on aspirin 81mg daily. Recommend stress test as outpatient. Follow-up in 1 week or sooner if symptoms worsen. Patient education provided regarding warning signs. Patient verbalized understanding.""",

    "routine_checkup": """Patient is a 32-year-old female presenting for annual physical examination. Patient reports feeling well with no current complaints. Patient states she exercises regularly and maintains a balanced diet. No new medications since last visit. Patient denies any allergies.

Vital signs: BP 118/76 mmHg, HR 72 bpm, Temp 98.2°F, RR 14, Weight 145 lbs, Height 5'6".

Physical examination shows patient is well-appearing and in no distress. HEENT examination normal. Cardiovascular examination reveals regular rate and rhythm. Respiratory examination shows clear lung fields bilaterally. Abdominal examination soft and non-tender.

Assessment: Healthy adult female, routine preventive care visit.

Plan: Continue current lifestyle modifications. Update immunizations as needed. Schedule mammogram screening. Provided education on preventive health measures. Follow-up in one year for routine physical.""",

    "upper_respiratory": """Patient is a 28-year-old male presenting with complaint of sore throat and nasal congestion for 3 days. Patient reports mild fever at home, maximum temperature 100.4°F. Patient states symptoms started after attending a large gathering. Patient denies difficulty breathing or severe pain. Patient has been taking over-the-counter ibuprofen with some relief.

Vital signs: BP 124/82 mmHg, HR 88 bpm, Temp 99.8°F, RR 16, O2 sat 99% on room air.

Physical examination reveals patient appears mildly ill but not in distress. Oropharynx shows erythema without exudates. Nasal mucosa appears inflamed. Lungs clear bilaterally. No lymphadenopathy noted.

Assessment: Viral upper respiratory infection, likely rhinovirus.

Plan: Supportive care with rest and hydration. Continue ibuprofen for fever and discomfort. Recommend saltwater gargles for throat pain. Patient advised to return if symptoms worsen or persist beyond 7-10 days. Patient education provided on respiratory hygiene. No antibiotics indicated at this time.""",
}


def get_sample_note(note_type: str = "chest_pain") -> str:
    """
    Get a sample clinical note.
    
    Args:
        note_type: Type of note to retrieve
        
    Returns:
        Sample clinical note text
    """
    return SAMPLE_NOTES.get(note_type, SAMPLE_NOTES["chest_pain"])


def list_sample_types() -> list:
    """
    List available sample note types.
    
    Returns:
        List of available note types
    """
    return list(SAMPLE_NOTES.keys())
