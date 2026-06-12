#!/usr/bin/env python3
"""Generate lib/l10n/app_strings_content.dart from translation tables."""
from __future__ import annotations

from pathlib import Path

from pathway_bundle import all_extra

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "lib" / "l10n" / "app_strings_content.dart"

# fmt: off
CONTENT: dict[str, dict[str, str]] = {
    # ── F2 symptom checker ──────────────────────────────────────────────
    "sectionGeneral": {"en": "General", "hi": "सामान्य", "kn": "ಸಾಮಾನ್ಯ"},
    "sectionSkin": {"en": "Skin", "hi": "त्वचा", "kn": "ಚರ್ಮ"},
    "sectionRespiratory": {"en": "Respiratory", "hi": "श्वसन", "kn": "ಶ್ವಾಸಕೋಶ"},
    "sectionReproductive": {"en": "Reproductive", "hi": "प्रजनन", "kn": "ಸಂತಾನೋತ್ಪತ್ತಿ"},
    "smartGuidance": {"en": "Smart Guidance", "hi": "स्मार्ट मार्गदर्शन", "kn": "ಸ್ಮಾರ್ಟ್ ಮಾರ್ಗದರ್ಶನ"},
    "useCameraScan": {"en": "📸 Use camera scan for visible diseases", "hi": "📸 दिखने वाले रोगों के लिए कैमरा स्कैन करें", "kn": "📸 ಗೋಚರಿಸುವ ರೋಗಗಳಿಗೆ ಕ್ಯಾಮೆರಾ ಸ್ಕ್ಯಾನ್ ಬಳಸಿ"},
    "useSymptomCheckerIf": {"en": "📋 Use symptom checker if:", "hi": "📋 लक्षण जांचकर्ता इन स्थितियों में:", "kn": "📋 ಈ ಸಂದರ್ಭಗಳಲ್ಲಿ ಲಕ್ಷಣ ಪರಿಶೀಲಕ ಬಳಸಿ:"},
    "noVisibleSymptoms": {"en": "• no visible symptoms", "hi": "• कोई दिखने वाले लक्षण नहीं", "kn": "• ಗೋಚರ ಲಕ್ಷಣಗಳಿಲ್ಲ"},
    "imageUnclear": {"en": "• image result is unclear", "hi": "• छवि परिणाम स्पष्ट नहीं", "kn": "• ಚಿತ್ರ ಫಲಿತಾಂಶ ಸ್ಪಷ್ಟವಿಲ್ಲ"},
    "internalDisease": {"en": "• disease is internal", "hi": "• रोग आंतरिक है", "kn": "• ರೋಗ ಆಂತರಿಕವಾಗಿದೆ"},
    "voiceInput": {"en": "Voice Input", "hi": "आवाज़ इनपुट", "kn": "ಧ್ವನಿ ಇನ್‌ಪುಟ್"},
    "stopListening": {"en": "Stop Listening", "hi": "सुनना बंद करें", "kn": "ಕೇಳುವುದನ್ನು ನಿಲ್ಲಿಸಿ"},
    "useVoice": {"en": "Use Voice", "hi": "आवाज़ का उपयोग करें", "kn": "ಧ್ವನಿ ಬಳಸಿ"},
    "voiceExample": {"en": "Example: cow has fever and weight loss", "hi": "उदाहरण: गाय को बुखार और वजन घटा है", "kn": "ಉದಾಹರಣೆ: ಹಸುವಿಗೆ ಜ್ವರ ಮತ್ತು ತೂಕ ಇಳಿಕೆ"},
    "lowConfidenceSymptoms": {"en": "Low confidence detected. Please confirm using symptoms.", "hi": "कम विश्वास मिला। कृपया लक्षणों से पुष्टि करें।", "kn": "ಕಡಿಮೆ ವಿಶ್ವಾಸ ಪತ್ತೆಯಾಗಿದೆ. ದಯವಿಟ್ಟು ಲಕ್ಷಣಗಳಿಂದ ದೃಢೀಕರಿಸಿ."},
    "fusionBannerPrefix": {"en": "Image scan suggested ", "hi": "छवि स्कैन ने सुझाया ", "kn": "ಚಿತ್ರ ಸ್ಕ್ಯಾನ್ ಸೂಚಿಸಿದೆ "},
    "fusionBannerSuffix": {"en": "). Select the symptoms you've noticed to refine this.", "hi": "). इसे बेहतर बनाने के लिए देखे गए लक्षण चुनें।", "kn": "). ಇದನ್ನು ಸುಧಾರಿಸಲು ನೀವು ಗಮನಿಸಿದ ಲಕ್ಷಣಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ."},
    "selectMin2Symptoms": {"en": "Please select at least 2 symptoms you have observed in your animal.", "hi": "कृपया अपने पशु में देखे गए कम से कम 2 लक्षण चुनें।", "kn": "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಜಾನುವಾರಿನಲ್ಲಿ ಗಮನಿಸಿದ ಕನಿಷ್ಠ 2 ಲಕ್ಷಣಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ."},
    "couldNotAnalyzeSymptoms": {"en": "Could not analyze symptoms.", "hi": "लक्षण विश्लेषित नहीं हो सके।", "kn": "ಲಕ್ಷಣಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ."},
    "missingFusionScores": {"en": "Missing symptom scores for fusion. Please retry.", "hi": "फ़्यूज़न के लिए लक्षण स्कोर गायब। पुनः प्रयास करें।", "kn": "ಫ್ಯೂಷನ್‌ಗಾಗಿ ಲಕ್ಷಣ ಸ್ಕೋರ್‌ಗಳು ಕಾಣೆಯಾಗಿವೆ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."},
    "voiceError": {"en": "Voice error: {msg}. Check microphone permission and Google speech service.", "hi": "आवाज़ त्रुटि: {msg}. माइक्रोफ़ोन अनुमति और Google speech service जाँचें।", "kn": "ಧ್ವನಿ ದೋಷ: {msg}. ಮೈಕ್ರೋಫೋನ್ ಅನುಮತಿ ಮತ್ತು Google speech service ಪರಿಶೀಲಿಸಿ."},
    "speechUnavailable": {"en": "Speech recognition is unavailable. Enable microphone permission and install/update Google Speech Services.", "hi": "वॉइस पहचान उपलब्ध नहीं। माइक्रोफ़ोन अनुमति चालू करें और Google Speech Services इंस्टॉल/अपडेट करें।", "kn": "ಮಾತು ಗುರುತಿಸುವಿಕೆ ಲಭ್ಯವಿಲ್ಲ. ಮೈಕ್ರೋಫೋನ್ ಅನುಮತಿ ಸಕ್ರಿಯಗೊಳಿಸಿ ಮತ್ತು Google Speech Services ಸ್ಥಾಪಿಸಿ/ನವೀಕರಿಸಿ."},
    "fullRiskGuidanceDesc": {"en": "Get full risk assessment, transmission pathways, and watch calendar for the top prediction.", "hi": "शीर्ष पूर्वानुमान के लिए पूर्ण जोखिम मूल्यांकन, संचरण मार्ग और वॉच कैलेंडर पाएँ।", "kn": "ಮೇಲಿನ ಭವಿಷ್ಯಕ್ಕಾಗಿ ಸಂಪೂರ್ಣ ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ, ಪ್ರಸರಣ ಮಾರ್ಗಗಳು ಮತ್ತು ವಾಚ್ ಕ್ಯಾಲೆಂಡರ್ ಪಡೆಯಿರಿ."},
    "noZoonoticBody": {"en": "The symptoms you selected are common to many general illnesses and are not specific to any zoonotic disease. Your animal may be experiencing a general health issue.", "hi": "आपके चुने लक्षण कई सामान्य बीमारियों में होते हैं और किसी जूनोटिक रोग से विशिष्ट नहीं हैं। आपका पशु सामान्य स्वास्थ्य समस्या से ग्रस्त हो सकता है।", "kn": "ನೀವು ಆಯ್ಕೆಮಾಡಿದ ಲಕ್ಷಣಗಳು ಅನೇಕ ಸಾಮಾನ್ಯ ಅನಾರೋಗ್ಯಗಳಲ್ಲಿ ಕಾಣಿಸುತ್ತವೆ ಮತ್ತು ಯಾವುದೇ ಜೂನೋಟಿಕ್ ರೋಗಕ್ಕೆ ವಿಶೇಷವಲ್ಲ. ನಿಮ್ಮ ಜಾನುವಾರು ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಸಮಸ್ಯೆಯನ್ನು ಅನುಭವಿಸುತ್ತಿರಬಹುದು."},
    "consultVetGeneral": {"en": "We recommend consulting a local veterinarian to check on your animal's general health.", "hi": "हम सुझाव देते हैं कि अपने पशु के सामान्य स्वास्थ्य के लिए स्थानीय पशु चिकित्सक से परामर्श करें।", "kn": "ನಿಮ್ಮ ಜಾನುವಾರಿನ ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಪರಿಶೀಲನೆಗಾಗಿ ಸ್ಥಳೀಯ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಲು ಶಿಫಾರಸು ಮಾಡುತ್ತೇವೆ."},
    "hideNearbyVets": {"en": "Hide nearby vets", "hi": "पास के पशु चिकित्सक छिपाएँ", "kn": "ಹತ್ತಿರದ ಪಶುವೈದ್ಯರನ್ನು ಮರೆಮಾಡಿ"},
    "showNearbyVets": {"en": "Show nearby vets", "hi": "पास के पशु चिकित्सक दिखाएँ", "kn": "ಹತ್ತಿರದ ಪಶುವೈದ್ಯರನ್ನು ತೋರಿಸಿ"},
    "findNearbyVets": {"en": "Find Nearby Vets", "hi": "पास के पशु चिकित्सक खोजें", "kn": "ಹತ್ತಿರದ ಪಶುವೈದ್ಯರನ್ನು ಹುಡುಕಿ"},
    "stillWantWatch": {"en": "Still want to keep a health watch?", "hi": "अभी भी स्वास्थ्य निगरानी रखना चाहते हैं?", "kn": "ಇನ್ನೂ ಆರೋಗ್ಯ ಮೇಲ್ವಿಚಾರಣೆ ಇಟ್ಟುಕೊಳ್ಳಲು ಬಯಸುವಿರಾ?"},
    "watchSheetDesc": {"en": "A watch calendar tracks whether new symptoms appear in the coming days. Tap below to start one.", "hi": "वॉच कैलेंडर आने वाले दिनों में नए लक्षण दिखने पर नज़र रखता है। शुरू करने के लिए नीचे टैप करें।", "kn": "ವಾಚ್ ಕ್ಯಾಲೆಂಡರ್ ಮುಂದಿನ ದಿನಗಳಲ್ಲಿ ಹೊಸ ಲಕ್ಷಣಗಳು ಕಾಣಿಸುತ್ತವೆಯೇ ಎಂದು ಟ್ರ್ಯಾಕ್ ಮಾಡುತ್ತದೆ. ಪ್ರಾರಂಭಿಸಲು ಕೆಳಗೆ ಟ್ಯಾಪ್ ಮಾಡಿ."},
    # symptom labels + hints
    "symptom_fever": {"en": "Fever", "hi": "बुखार", "kn": "ಜ್ವರ"},
    "symptom_fever_hint": {"en": "Body feels hotter than normal", "hi": "शरीर सामान्य से अधिक गर्म लगता है", "kn": "ದೇಹ ಸಾಮಾನ್ಯಕ್ಕಿಂತ ಹೆಚ್ಚು ಬಿಸಿಯಾಗಿ ಅನುಭವಿಸುತ್ತದೆ"},
    "symptom_weight_loss": {"en": "Weight loss", "hi": "वजन घटना", "kn": "ತೂಕ ಇಳಿಕೆ"},
    "symptom_weight_loss_hint": {"en": "Noticeable drop in body condition", "hi": "शरीर की स्थिति में स्पष्ट गिरावट", "kn": "ದೇಹ ಸ್ಥಿತಿಯಲ್ಲಿ ಗಮನಾರ್ಹ ಇಳಿಕೆ"},
    "symptom_lethargy": {"en": "Lethargy", "hi": "सुस्ती", "kn": "ಸೋಮಾರಿತನ"},
    "symptom_lethargy_hint": {"en": "Animal appears weak or inactive", "hi": "पशु कमज़ोर या सुस्त दिखता है", "kn": "ಜಾನುವಾರು ದುರ್ಬಲ ಅಥವಾ ನಿಷ್ಕ್ರಿಯವಾಗಿ ಕಾಣುತ್ತದೆ"},
    "symptom_diarrhea": {"en": "Diarrhea", "hi": "दस्त", "kn": "ಅತಿಸಾರ"},
    "symptom_diarrhea_hint": {"en": "Frequent loose stool", "hi": "बार-बार पतला मल", "kn": "ಆಗಾಗ್ಗೆ ವಿರೇಚನ"},
    "symptom_skin_lesions": {"en": "Skin lesions", "hi": "त्वचा के घाव", "kn": "ಚರ್ಮದ ಗಾಯಗಳು"},
    "symptom_skin_lesions_hint": {"en": "Visible sores or abnormal skin patches", "hi": "दिखने वाले घाव या असामान्य त्वचा धब्बे", "kn": "ಗೋಚರ ಗಾಯಗಳು ಅಥವಾ ಅಸಾಮಾನ್ಯ ಚರ್ಮ ಪ್ಯಾಚ್‌ಗಳು"},
    "symptom_blisters": {"en": "Blisters", "hi": "फफोले", "kn": "ಗುಳ್ಳೆಗಳು"},
    "symptom_blisters_hint": {"en": "Fluid-filled bumps on skin or mouth", "hi": "त्वचा या मुँह पर पानी भरे फफोले", "kn": "ಚರ್ಮ ಅಥವಾ ಬಾಯಿಯಲ್ಲಿ ದ್ರವ ತುಂಬಿದ ಗುಳ್ಳೆಗಳು"},
    "symptom_jaundice": {"en": "Jaundice", "hi": "पीलिया", "kn": "ಕಾಮಾಲೆ"},
    "symptom_jaundice_hint": {"en": "Yellowish eyes or skin", "hi": "पीली आँखें या त्वचा", "kn": "ಹಳದಿ ಕಣ್ಣುಗಳು ಅಥವಾ ಚರ್ಮ"},
    "symptom_limping": {"en": "Limping", "hi": "लंगड़ाना", "kn": "ಲಂಗು"},
    "symptom_limping_hint": {"en": "Trouble walking normally", "hi": "सामान्य चलने में परेशानी", "kn": "ಸಾಮಾನ್ಯವಾಗಿ ನಡೆಯಲು ತೊಂದರೆ"},
    "symptom_coughing": {"en": "Coughing", "hi": "खाँसी", "kn": "ಕೆಮ್ಮು"},
    "symptom_coughing_hint": {"en": "Persistent coughing signs", "hi": "लगातार खाँसी के संकेत", "kn": "ನಿರಂತರ ಕೆಮ್ಮಿನ ಲಕ್ಷಣಗಳು"},
    "symptom_nasal_discharge": {"en": "Nasal discharge", "hi": "नाक से स्राव", "kn": "ಮೂಗಿನ ಸ್ರಾವ"},
    "symptom_nasal_discharge_hint": {"en": "Runny nose or mucus", "hi": "बहती नाक या बलगम", "kn": "ಒಸರುವ ಮೂಗು ಅಥವಾ ಲೋಹ"},
    "symptom_eye_discharge": {"en": "Eye discharge", "hi": "आँख से स्राव", "kn": "ಕಣ್ಣಿನ ಸ್ರಾವ"},
    "symptom_eye_discharge_hint": {"en": "Watery or sticky eye fluid", "hi": "आँख से पानी या चिपचिपा तरल", "kn": "ಕಣ್ಣಿನಿಂದ ನೀರು ಅಥವಾ ಅಂಟುವ ದ್ರವ"},
    "symptom_breathing_difficulty": {"en": "Breathing difficulty", "hi": "साँस लेने में कठिनाई", "kn": "ಉಸಿರಾಟದ ತೊಂದರೆ"},
    "symptom_breathing_difficulty_hint": {"en": "Fast or labored breathing", "hi": "तेज़ या मुश्किल से साँस लेना", "kn": "ವೇಗವಾದ ಅಥವಾ ಕಷ್ಟದ ಉಸಿರಾಟ"},
    "symptom_milk_drop": {"en": "Milk drop", "hi": "दूध में कमी", "kn": "ಹಾಲು ಇಳಿಕೆ"},
    "symptom_milk_drop_hint": {"en": "Sudden reduction in milk yield", "hi": "दूध उत्पादन में अचानक कमी", "kn": "ಹಾಲು ಉತ್ಪಾದನೆಯಲ್ಲಿ ಅಚಾನಕ ಇಳಿಕೆ"},
    "symptom_abortion": {"en": "Abortion", "hi": "गर्भपात", "kn": "ಗರ್ಭಪಾತ"},
    "symptom_abortion_hint": {"en": "Pregnancy loss signs", "hi": "गर्भ खोने के संकेत", "kn": "ಗರ್ಭ ನಷ್ಟದ ಲಕ್ಷಣಗಳು"},
    "symptom_reproductive_failure": {"en": "Reproductive failure", "hi": "प्रजनन विफलता", "kn": "ಸಂತಾನೋತ್ಪತ್ತಿ ವೈಫಲ್ಯ"},
    "symptom_reproductive_failure_hint": {"en": "Difficulty conceiving or maintaining pregnancy", "hi": "गर्भधारण या गर्भ बनाए रखने में कठिनाई", "kn": "ಗರ್ಭಧಾರಣೆ ಅಥವಾ ಗರ್ಭ ಉಳಿಸಿಕೊಳ್ಳಲು ತೊಂದರೆ"},
    "symptom_blood_from_orifices": {"en": "Blood from orifices", "hi": "छिद्रों से खून", "kn": "ರಂಧ್ರಗಳಿಂದ ರಕ್ತ"},
    "symptom_blood_from_orifices_hint": {"en": "Bleeding from nose, mouth, or genital area", "hi": "नाक, मुँह या जननांग से खून आना", "kn": "ಮೂಗು, ಬಾಯಿ ಅಥವಾ ಜನನಾಂಗ ಪ್ರದೇಶದಿಂದ ರಕ್ತಸ್ರಾವ"},
    "symptom_sudden_death": {"en": "Sudden death", "hi": "अचानक मौत", "kn": "ಅಚಾನಕ ಸಾವು"},
    "symptom_sudden_death_hint": {"en": "Unexpected death in herd", "hi": "झुंड में अचानक मौत", "kn": "ಕೂಪದಲ್ಲಿ ಅನಿರೀಕ್ಷಿತ ಸಾವು"},
    "symptom_swollen_lymph_nodes": {"en": "Swollen lymph nodes", "hi": "सूजे लसीका ग्रंथि", "kn": "ಊತವಾದ ಲಸಿಕಾ ಗ್ರಂಥಿಗಳು"},
    "symptom_swollen_lymph_nodes_hint": {"en": "Swelling around jaw/neck nodes", "hi": "जबड़े/गर्दन के ग्रंथियों में सूजन", "kn": "ದವಡೆ/ಕುತ್ತಿಗೆ ಗ್ರಂಥಿಗಳ ಸುತ್ತ ಊತ"},
    # ── F3 risk assessment ────────────────────────────────────────────
    "expQ_direct_contact": {"en": "Did you touch the cow directly without gloves?", "hi": "क्या आपने बिना दस्ताने गाय को सीधे छुआ?", "kn": "ನೀವು ಕೈಗವಸ್ ಇಲ್ಲದೆ ಹಸುವನ್ನು ನೇರವಾಗಿ ಮುಟ್ಟಿದ್ದೀರಾ?"},
    "expQ_raw_milk_meat": {"en": "Did your family drink raw milk or eat undercooked meat?", "hi": "क्या आपके परिवार ने कच्चा दूध पिया या अधपका मांस खाया?", "kn": "ನಿಮ್ಮ ಕುಟುಂಬ ಕಚ್ಚಾ ಹಾಲು ಕುಡಿದಿತ್ತೇ ಅಥವಾ ಅರ್ಧ ಬೇಯಿಸಿದ ಮಾಂಸ ತಿಂದಿತ್ತೇ?"},
    "expQ_open_wounds": {"en": "Do you have any open cuts or wounds on your hands?", "hi": "क्या आपके हाथों पर कोई खुले घाव हैं?", "kn": "ನಿಮ್ಮ ಕೈಗಳಲ್ಲಿ ಯಾವುದೇ ತೆರೆದ ಗಾಯಗಳಿವೆಯೇ?"},
    "expQ_children_contact": {"en": "Are there children under 10 in your household?", "hi": "क्या आपके घर में 10 वर्ष से कम उम्र के बच्चे हैं?", "kn": "ನಿಮ್ಮ ಮನೆಯಲ್ಲಿ 10 ವರ್ಷಕ್ಕಿಂತ ಕಡಿಮೆ ವಯಸ್ಸಿನ ಮಕ್ಕಳಿದ್ದಾರೆಯೇ?"},
    "expQ_elderly_pregnant": {"en": "Are there elderly or pregnant people in your household?", "hi": "क्या आपके घर में बुजुर्ग या गर्भवती लोग हैं?", "kn": "ನಿಮ್ಮ ಮನೆಯಲ್ಲಿ ವೃದ್ಧರು ಅಥವಾ ಗರ್ಭಿಣಿ ಮಹಿಳೆಯರು ಇದ್ದಾರೆಯೇ?"},
    "expQ_unvaccinated": {"en": "Is anyone unvaccinated against this disease?", "hi": "क्या कोई इस रोग के खिलाफ टीकाकृत नहीं है?", "kn": "ಯಾರಾದರೂ ಈ ರೋಗದ ವಿರುದ್ಧ ಲಸಿಕೆ ಪಡೆದಿಲ್ಲವೇ?"},
    "expLabel_direct_contact": {"en": "Direct contact without gloves", "hi": "बिना दस्ताने सीधा संपर्क", "kn": "ಕೈಗವಸ್ ಇಲ್ಲದೆ ನೇರ ಸಂಪರ್ಕ"},
    "expLabel_raw_milk_meat": {"en": "Raw milk or undercooked meat", "hi": "कच्चा दूध या अधपका मांस", "kn": "ಕಚ್ಚಾ ಹಾಲು ಅಥವಾ ಅರ್ಧ ಬೇಯಿಸಿದ ಮಾಂಸ"},
    "expLabel_open_wounds": {"en": "Open cuts or wounds", "hi": "खुले घाव", "kn": "ತೆರೆದ ಗಾಯಗಳು"},
    "expLabel_children_contact": {"en": "Children under 10 in household", "hi": "घर में 10 वर्ष से कम बच्चे", "kn": "ಮನೆಯಲ್ಲಿ 10 ವರ್ಷಕ್ಕಿಂತ ಕಡಿಮೆ ಮಕ್ಕಳು"},
    "expLabel_elderly_pregnant": {"en": "Elderly or pregnant in household", "hi": "घर में बुजुर्ग या गर्भवती", "kn": "ಮನೆಯಲ್ಲಿ ವೃದ್ಧರು ಅಥವಾ ಗರ್ಭಿಣಿ"},
    "expLabel_unvaccinated": {"en": "Unvaccinated household member", "hi": "बिना टीके का परिवार सदस्य", "kn": "ಲಸಿಕೆ ಪಡೆಯದ ಕುಟುಂಬ ಸದಸ್ಯ"},
    "contrib_direct_contact": {"en": "Direct contact", "hi": "सीधा संपर्क", "kn": "ನೇರ ಸಂಪರ್ಕ"},
    "contrib_raw_milk_meat": {"en": "Raw milk/meat", "hi": "कच्चा दूध/मांस", "kn": "ಕಚ್ಚಾ ಹಾಲು/ಮಾಂಸ"},
    "contrib_open_wounds": {"en": "Open wounds", "hi": "खुले घाव", "kn": "ತೆರೆದ ಗಾಯಗಳು"},
    "contrib_children_contact": {"en": "Children <10", "hi": "बच्चे <10", "kn": "ಮಕ್ಕಳು <10"},
    "contrib_elderly_pregnant": {"en": "Elderly/pregnant", "hi": "बुजुर्ग/गर्भवती", "kn": "ವೃದ್ಧ/ಗರ್ಭಿಣಿ"},
    "contrib_unvaccinated": {"en": "Unvaccinated", "hi": "बिना टीके", "kn": "ಲಸಿಕೆ ಪಡೆಯದ"},
    "noFactorIncreasedRisk": {"en": "No specific factor increased risk.", "hi": "कोई विशेष कारक जोखिम नहीं बढ़ाया।", "kn": "ಯಾವುದೇ ನಿರ್ದಿಷ್ಟ ಅಂಶ ಅಪಾಯವನ್ನು ಹೆಚ್ಚಿಸಲಿಲ್ಲ."},
    "riskScoreLabel": {"en": "Risk score (0–100)", "hi": "जोखिम स्कोर (0–100)", "kn": "ಅಪಾಯ ಸ್ಕೋರ್ (0–100)"},
    "riskUnavailable": {"en": "Risk assessment is not available for this result. Try adding symptoms or rescanning the animal.", "hi": "इस परिणाम के लिए जोखिम मूल्यांकन उपलब्ध नहीं। लक्षण जोड़ें या पशु को पुनः स्कैन करें।", "kn": "ಈ ಫಲಿತಾಂಶಕ್ಕೆ ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ ಲಭ್ಯವಿಲ್ಲ. ಲಕ್ಷಣಗಳನ್ನು ಸೇರಿಸಿ ಅಥವಾ ಜಾನುವಾರನ್ನು ಮತ್ತೆ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ."},
    "couldNotComputeRisk": {"en": "Could not compute risk right now. Please retry.", "hi": "अभी जोखिम की गणना नहीं हो सकी। पुनः प्रयास करें।", "kn": "ಈಗ ಅಪಾಯ ಲೆಕ್ಕಾಚಾರ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."},
    "reportSubmitLocationError": {"en": "Could not submit report. Check location and try again.", "hi": "रिपोर्ट जमा नहीं हो सकी। स्थान जाँचें और पुनः प्रयास करें।", "kn": "ವರದಿ ಸಲ್ಲಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಸ್ಥಳ ಪರಿಶೀಲಿಸಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."},
    "reportSubmitSuccess": {"en": "Report submitted successfully.", "hi": "रिपोर्ट सफलतापूर्वक जमा हो गई।", "kn": "ವರದಿ ಯಶಸ್ವಿಯಾಗಿ ಸಲ್ಲಿಸಲಾಗಿದೆ."},
    "reportSubmitRetry": {"en": "Could not submit report. Please try again.", "hi": "रिपोर्ट जमा नहीं हो सकी। पुनः प्रयास करें।", "kn": "ವರದಿ ಸಲ್ಲಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ."},
    "animalCareSteps": {"en": "Animal Care Steps", "hi": "पशु देखभाल कदम", "kn": "ಜಾನುವಾರು ಆರೈಕೆ ಹಂತಗಳು"},
    "animalCareTap": {"en": "Tap to see what to do with your cow", "hi": "अपनी गाय के लिए क्या करें देखने के लिए टैप करें", "kn": "ನಿಮ್ಮ ಹಸುವಿಗೆ ಏನು ಮಾಡಬೇಕು ಎಂದು ನೋಡಲು ಟ್ಯಾಪ್ ಮಾಡಿ"},
    "animalCareUnavailable": {"en": "Animal care guidance is not available for this disease yet.", "hi": "इस रोग के लिए पशु देखभाल मार्गदर्शन अभी उपलब्ध नहीं।", "kn": "ಈ ರೋಗಕ್ಕೆ ಜಾನುವಾರು ಆರೈಕೆ ಮಾರ್ಗದರ್ಶನ ಇನ್ನೂ ಲಭ್ಯವಿಲ್ಲ."},
    "careImmediate": {"en": "Do right now", "hi": "अभी करें", "kn": "ಈಗ ಮಾಡಿ"},
    "careDoNot": {"en": "Do NOT do", "hi": "न करें", "kn": "ಮಾಡಬೇಡಿ"},
    "careVetAction": {"en": "Call a vet for", "hi": "पशु चिकित्सक को बुलाएँ", "kn": "ಪಶುವೈದ್ಯರನ್ನು ಕರೆ ಮಾಡಿ"},
    "careRecovery": {"en": "What to expect", "hi": "क्या अपेक्षा करें", "kn": "ಏನನ್ನು ನಿರೀಕ್ಷಿಸಬಹುದು"},
    "riskActionLow": {"en": "Monitor the cow. Wash hands thoroughly after any contact.", "hi": "गाय पर नज़र रखें। संपर्क के बाद हाथ अच्छी तरह धोएँ।", "kn": "ಹಸುವನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ. ಯಾವುದೇ ಸಂಪರ್ಕದ ನಂತರ ಕೈಗಳನ್ನು ಚೆನ್ನಾಗಿ ಕುಳಿಸಿ."},
    "riskActionModerate": {"en": "See a doctor within 3 days. Avoid direct contact without gloves.", "hi": "3 दिनों में डॉक्टर से मिलें। बिना दस्ताने सीधा संपर्क से बचें।", "kn": "3 ದಿನಗಳಲ್ಲಿ ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ. ಕೈಗವಸ್ ಇಲ್ಲದೆ ನೇರ ಸಂಪರ್ಕ ತಪ್ಪಿಸಿ."},
    "riskActionHigh": {"en": "See a doctor today and avoid further contact with the animal.", "hi": "आज डॉक्टर से मिलें और पशु से और संपर्क से बचें।", "kn": "ಇಂದು ವೈದ್ಯರನ್ನು ಭೇಟಿ ಮಾಡಿ ಮತ್ತು ಜಾನುವಾರಿನೊಂದಿಗೆ ಮತ್ತಷ್ಟು ಸಂಪರ್ಕ ತಪ್ಪಿಸಿ."},
    "riskActionCritical": {"en": "Go to a hospital immediately and call a government vet now.", "hi": "तुरंत अस्पताल जाएँ और अभी सरकारी पशु चिकित्सक को बुलाएँ।", "kn": "ತಕ್ಷಣ ಆಸ್ಪತ್ರೆಗೆ ಹೋಗಿ ಮತ್ತು ಈಗ ಸರ್ಕಾರಿ ಪಶುವೈದ್ಯರನ್ನು ಕರೆ ಮಾಡಿ."},
    # F1 result advisory (shown on path to F3)
    "riskTextRingworm": {"en": "Potential zoonotic risk. Avoid direct contact without gloves.", "hi": "संभावित जूनोटिक जोखिम। बिना दस्ताने सीधा संपर्क से बचें।", "kn": "ಸಂಭಾವ್ಯ ಜೂನೋಟಿಕ್ ಅಪಾಯ. ಕೈಗವಸ್ ಇಲ್ಲದೆ ನೇರ ಸಂಪರ್ಕ ತಪ್ಪಿಸಿ."},
    "riskTextFmd": {"en": "Low direct human risk, but highly contagious among livestock.", "hi": "मानवों के लिए कम सीधा जोखिम, लेकिन पशुओं में अत्यधिक संक्रामक।", "kn": "ಮಾನವರಿಗೆ ಕಡಿಮೆ ನೇರ ಅಪಾಯ, ಆದರೆ ಜಾನುವಾರುಗಳಲ್ಲಿ ಹೆಚ್ಚು ಸಾಕ್ಷಾತ್ಕಾರಿ."},
    "riskTextHealthy": {"en": "No immediate zoonotic risk detected.", "hi": "कोई तत्काल जूनोटिक जोखिम नहीं मिला।", "kn": "ತಕ್ಷಣದ ಜೂನೋಟಿಕ್ ಅಪಾಯ ಪತ್ತೆಯಾಗಿಲ್ಲ."},
    "riskTextUncertain": {"en": "Unable to determine reliably. Follow standard safety practices.", "hi": "विश्वसनीय रूप से निर्धारित नहीं हो सका। मानक सुरक्षा अभ्यास अपनाएँ।", "kn": "ವಿಶ್ವಾಸಾರ್ಹವಾಗಿ ನಿರ್ಧರಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಪ್ರಮಾಣಿತ ಸುರಕ್ಷತಾ ಪದ್ಧತಿಗಳನ್ನು ಅನುಸರಿಸಿ."},
    "riskTextDefault": {"en": "Consult a veterinarian to assess potential zoonotic exposure.", "hi": "संभावित जूनोटिक संपर्क का मूल्यांकन करने के लिए पशु चिकित्सक से सलाह लें।", "kn": "ಸಂಭಾವ್ಯ ಜೂನೋಟಿಕ್ ಸಂಪರ್ಕವನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡಲು ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ."},
    "adviceHealthy": {"en": "Maintain hygiene, regular vaccination, and periodic checkups.", "hi": "स्वच्छता, नियमित टीकाकरण और समय-समय पर जाँच बनाए रखें।", "kn": "ನೈರ್ಮಲ್ಯ, ನಿಯಮಿತ ಲಸಿಕೆ ಮತ್ತು ಆವರ್ತಕ ಪರಿಶೀಲನೆಗಳನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."},
    "adviceUncertain": {"en": "Retake a clear image in better lighting and try again.", "hi": "बेहतर रोशनी में स्पष्ट तस्वीर लें और पुनः प्रयास करें।", "kn": "ಉತ್ತಮ ಬೆಳಕಿನಲ್ಲಿ ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಮತ್ತೆ ತೆಗೆದು ಪ್ರಯತ್ನಿಸಿ."},
    "adviceDefault": {"en": "Isolate the animal, sanitize equipment, and contact a vet quickly.", "hi": "पशु को अलग करें, उपकरण साफ़ करें और जल्दी पशु चिकित्सक से संपर्क करें।", "kn": "ಜಾನುವಾರನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ, ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ ಮತ್ತು ಬೇಗ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ."},
    # ── F5 watch calendar ───────────────────────────────────────────────
    "timelineHint": {"en": "Orange shows the early period when illness most often begins. The line marks today.", "hi": "नारंगी वह प्रारंभिक अवधि दिखाता है जब बीमारी अक्सर शुरू होती है। रेखा आज को दर्शाती है।", "kn": "ಕಿತ್ತಳೆ ಬಣ್ಣದಲ್ಲಿ ಅನಾರೋಗ್ಯ ಹೆಚ್ಚಾಗಿ ಪ್ರಾರಂಭವಾಗುವ ಆರಂಭಿಕ ಅವಧಿ ತೋರಿಸುತ್ತದೆ. ರೇಖೆ ಇಂದನ್ನು ಸೂಚಿಸುತ್ತದೆ."},
    "dailyReminderHelp": {"en": "Daily reminder time", "hi": "दैनिक अनुस्मारक समय", "kn": "ದೈನಂದಿನ ಜ್ಞಾಪನೆ ಸಮಯ"},
    "dailyAlertAt": {"en": "Daily alert at {time} during the watch period", "hi": "निगरानी अवधि में {time} पर दैनिक अलर्ट", "kn": "ಮೇಲ್ವಿಚಾರಣೆ ಅವಧಿಯಲ್ಲಿ {time} ನಲ್ಲಿ ದೈನಂದಿನ ಎಚ್ಚರಿಕೆ"},
    "changeTime": {"en": "Change time ({time})", "hi": "समय बदलें ({time})", "kn": "ಸಮಯ ಬದಲಾಯಿಸಿ ({time})"},
    "notificationTitle": {"en": "LivestockGuard", "hi": "लाइवस्टॉकगार्ड", "kn": "ಲೈವ್‌ಸ್ಟಾಕ್‌ಗಾರ್ಡ್"},
    "notificationBody": {"en": "Check yourself for {symptoms}. Tap to open your report.", "hi": "{symptoms} के लिए खुद की जाँच करें। रिपोर्ट खोलने के लिए टैप करें।", "kn": "{symptoms} ಗಾಗಿ ನಿಮ್ಮನ್ನು ಪರಿಶೀಲಿಸಿ. ವರದಿ ತೆರೆಯಲು ಟ್ಯಾಪ್ ಮಾಡಿ."},
    "symptomSheetHint": {"en": "Check anything that applies right now. You can still get a report if nothing is checked.", "hi": "जो भी अभी लागू हो उसे चुनें। कुछ भी न चुनने पर भी रिपोर्ट मिल सकती है।", "kn": "ಈಗ ಅನ್ವಯಿಸುವುದನ್ನು ಆಯ್ಕೆಮಾಡಿ. ಏನೂ ಆಯ್ಕೆಮಾಡದಿದ್ದರೂ ವರದಿ ಪಡೆಯಬಹುದು."},
    "watchGeneralDesc": {"en": "Started: {date}\nWatch for worsening symptoms over the next {days} days. This is a general health check-in — not tied to a specific zoonotic disease.", "hi": "शुरू: {date}\nअगले {days} दिनों में बढ़ते लक्षणों पर नज़र रखें। यह सामान्य स्वास्थ्य जाँच है — किसी विशिष्ट जूनोटिक रोग से नहीं जुड़ी।", "kn": "ಪ್ರಾರಂಭ: {date}\nಮುಂದಿನ {days} ದಿನಗಳಲ್ಲಿ ಹೆಚ್ಚುತ್ತಿರುವ ಲಕ್ಷಣಗಳನ್ನು ಗಮನಿಸಿ. ಇದು ಸಾಮಾನ್ಯ ಆರೋಗ್ಯ ಪರಿಶೀಲನೆ — ನಿರ್ದಿಷ್ಟ ಜೂನೋಟಿಕ್ ರೋಗಕ್ಕೆ ಬದ್ಧವಲ್ಲ."},
    "watchExposureDesc": {"en": "Exposure date: {date}\nStay alert for about {days} days after symptoms could begin.", "hi": "संपर्क तिथि: {date}\nलक्षण शुरू हो सकने के बाद लगभग {days} दिन सतर्क रहें।", "kn": "ಸಂಪರ್ಕ ದಿನಾಂಕ: {date}\nಲಕ್ಷಣಗಳು ಪ್ರಾರಂಭವಾಗಬಹುದಾದ ನಂತರ ಸುಮಾರು {days} ದಿನಗಳ ಕಾಲ ಎಚ್ಚರಿಕೆಯಿಂದ ಇರಿ."},
}
# fmt: on

def main() -> None:
    CONTENT.update(all_extra())
    langs = ("en", "hi", "kn")
    lines = [
        "// GENERATED by tool/generate_content_strings.py — do not edit by hand.",
        "class AppStringsContent {",
        "  const AppStringsContent._();",
        "",
    ]
    for lang in langs:
        lines.append(f"  static const Map<String, String> {lang} = {{")
        for key, tr in sorted(CONTENT.items()):
            val = (
                tr[lang]
                .replace("\\", "\\\\")
                .replace("'", "\\'")
                .replace("\n", "\\n")
                .replace("$", "\\$")
            )
            lines.append(f"    '{key}': '{val}',")
        lines.append("  };")
        lines.append("")
    lines.append("}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(CONTENT)} keys to {OUT}")

if __name__ == "__main__":
    main()
