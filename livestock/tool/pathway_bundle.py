"""Pathway nodes, routes, risk groups, animal guidance, watch symptoms — en/hi/kn."""

def _t(en: str, hi: str, kn: str) -> dict[str, str]:
    return {"en": en, "hi": hi, "kn": kn}


def pathway_entries() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    nodes = {
        "bruc": {
            "r0": _t("Infected cow (Brucella bacteria)", "संक्रमित गाय (ब्रूसेला बैक्टीरिया)", "ಸೋಂಕಿತ ಹಸು (ಬ್ರೂಸೆಲ್ಲಾ ಬ್ಯಾಕ್ಟೀರಿಯಾ)"),
            "r0e": _t("Brucella can be present in milk and birth fluids of infected cows.", "संक्रमित गायों के दूध और प्रसव द्रव में ब्रूसेला हो सकता है।", "ಸೋಂಕಿತ ಹಸುಗಳ ಹಾಲು ಮತ್ತು ಜನನ ದ್ರವಗಳಲ್ಲಿ ಬ್ರೂಸೆಲ್ಲಾ ಇರಬಹುದು."),
            "t0": _t("Raw milk / unpasteurised dairy", "कच्चा दूध / बिना पाश्चुरीकृत डेयरी", "ಕಚ್ಚಾ ಹಾಲು / ಪಾಸ್ಚರೀಕರಿಸದ ಡೈರಿ"),
            "t0e": _t("Brucella can survive in raw dairy and infect humans after ingestion.", "ब्रूसेला कच्चे डेयरी में जीवित रह सकता है और निगलने पर मनुष्यों को संक्रमित कर सकता है।", "ಬ್ರೂಸೆಲ್ಲಾ ಕಚ್ಚಾ ಡೈರಿಯಲ್ಲಿ ಬದುಕುತ್ತದೆ ಮತ್ತು ನುಂಗಿದ ನಂತರ ಮಾನವರನ್ನು ಸೋಂಕುಗೊಳಿಸಬಹುದು."),
            "t1": _t("Birth fluids / aborted fetus contact", "प्रसव द्रव / गर्भपात संपर्क", "ಜನನ ದ್ರವ / ಗರ್ಭಪಾತ ಸಂಪರ್ಕ"),
            "t1e": _t("Handling birthing materials without protection increases risk.", "बिना सुरक्षा प्रसव सामग्री छूने से जोखिम बढ़ता है।", "ರಕ್ಷಣೆಯಿಲ್ಲದೆ ಜನನ ಸಾಮಗ್ರಿಗಳನ್ನು ನಿರ್ವಹಿಸುವುದು ಅಪಾಯವನ್ನು ಹೆಚ್ಚಿಸುತ್ತದೆ."),
            "e0": _t("Mouth (ingestion)", "मुँह (निगलना)", "ಬಾಯಿ (ನುಂಗುವುದು)"),
            "e0e": _t("The bacteria enters via the digestive tract after consuming contaminated dairy.", "दूषित डेयरी खाने के बाद बैक्टीरिया पाचन तंत्र से प्रवेश करता है।", "ದೂಷಿತ ಡೈರಿ ಸೇವನೆಯ ನಂತರ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಜೀರ್ಣಕ್ರಿಯೆಯ ಮೂಲಕ ಪ್ರವೇಶಿಸುತ್ತದೆ."),
            "e1": _t("Open skin wounds", "खुले त्वचा घाव", "ತೆರೆದ ಚರ್ಮದ ಗಾಯಗಳು"),
            "e1e": _t("Cuts allow bacteria to enter the bloodstream directly.", "कट से बैक्टीरिया सीधे रक्तप्रवाह में प्रवेश कर सकता है।", "ಕತ್ತರಿಸುವಿಕೆಗಳು ಬ್ಯಾಕ್ಟೀರಿಯಾವನ್ನು ನೇರವಾಗಿ ರಕ್ತನಾಳಕ್ಕೆ ಪ್ರವೇಶಿಸಲು ಅನುಮತಿಸುತ್ತವೆ."),
            "o0": _t("Liver", "यकृत", "ಯಕೃತ್ತು"),
            "o0e": _t("Brucellosis may affect internal organs causing prolonged fever.", "ब्रूसेलोसिस आंतरिक अंगों को प्रभावित कर लंबे बुखार का कारण बन सकता है।", "ಬ್ರೂಸೆಲ್ಲೋಸಿಸ್ ಆಂತರಿಕ ಅಂಗಗಳನ್ನು ಬಾಧಿಸಿ ದೀರ್ಘಕಾಲದ ಜ್ವರಕ್ಕೆ ಕಾರಣವಾಗಬಹುದು."),
            "o1": _t("Bone marrow", "अस्थि मज्जा", "ಮೂಳೆ ಮಜ್ಜೆ"),
            "o1e": _t("Can cause weakness and long-lasting fatigue.", "कमज़ोरी और लंबे समय तक थकान का कारण बन सकता है।", "ದುರ್ಬಲತೆ ಮತ್ತು ದೀರ್ಘಕಾಲದ ಅಲಸತೆಗೆ ಕಾರಣವಾಗಬಹುದು."),
            "o2": _t("Reproductive system", "प्रजनन तंत्र", "ಸಂತಾನೋತ್ಪತ್ತಿ ವ್ಯವಸ್ಥೆ"),
            "o2e": _t("Higher concern for pregnant women due to miscarriage risk.", "गर्भपात के जोखिम के कारण गर्भवती महिलाओं के लिए अधिक चिंता।", "ಗರ್ಭಪಾತದ ಅಪಾಯದಿಂದಾಗಿ ಗರ್ಭಿಣಿ ಮಹಿಳೆಯರಿಗೆ ಹೆಚ್ಚಿನ ಕಾಳಜಿ."),
        },
        # Additional diseases abbreviated - full set added below via loop from master list
    }
    # Full disease node packs
    packs = {
        "lepto": {
            "r0": _t("Infected cow (Leptospira bacteria)", "संक्रमित गाय (लेप्टोस्पाइरा बैक्टीरिया)", "ಸೋಂಕಿತ ಹಸು (ಲೆಪ್ಟೋಸ್ಪೈರಾ ಬ್ಯಾಕ್ಟೀರಿಯಾ)"),
            "r0e": _t("Leptospira can be shed in urine of infected animals.", "संक्रमित जानवरों के मूत्र में लेप्टोस्पाइरा निकल सकता है।", "ಸೋಂಕಿತ ಪ್ರಾಣಿಗಳ ಮೂತ್ರದಲ್ಲಿ ಲೆಪ್ಟೋಸ್ಪೈರಾ ಬಿಡುಗಡೆಯಾಗಬಹುದು."),
            "t0": _t("Urine-contaminated water/soil", "मूत्र से दूषित पानी/मिट्टी", "ಮೂತ್ರದಿಂದ ಕಲುಷಿತ ನೀರು/ಮಣ್ಣು"),
            "t0e": _t("Walking or working in contaminated water exposes skin and mucous membranes.", "दूषित पानी में चलने या काम करने से त्वचा और श्लेष्मा झिल्ली संपर्क में आती है।", "ಕಲುಷಿತ ನೀರಿನಲ್ಲಿ ನಡೆಯುವುದು ಅಥವಾ ಕೆಲಸ ಮಾಡುವುದು ಚರ್ಮ ಮತ್ತು ಶ್ಲೇಷ್ಮ ಪೊರೆಯನ್ನು ಬಹಿರಂಗಪಡಿಸುತ್ತದೆ."),
            "t1": _t("Open wound contact with tissue", "घाव का संक्रमित ऊतक से संपर्क", "ಗಾಯದ ಸೋಂಕಿತ ಅಂಗಾಂಶ ಸಂಪರ್ಕ"),
            "t1e": _t("Cuts increase the chance of bacteria entering the body.", "कट से शरीर में बैक्टीरिया प्रवेश की संभावना बढ़ती है।", "ಕತ್ತರಿಸುವಿಕೆಗಳು ದೇಹಕ್ಕೆ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಪ್ರವೇಶಿಸುವ ಸಾಧ್ಯತೆಯನ್ನು ಹೆಚ್ಚಿಸುತ್ತವೆ."),
            "e0": _t("Broken skin / wounds", "फटी त्वचा / घाव", "ಹರಿದ ಚರ್ಮ / ಗಾಯಗಳು"),
            "e0e": _t("Even small cuts can allow infection.", "छोटे कट भी संक्रमण की अनुमति दे सकते हैं।", "ಸಣ್ಣ ಕತ್ತರಿಸುವಿಕೆಗಳೂ ಸೋಂಕುಗೊಳ್ಳಲು ಅನುಮತಿಸಬಹುದು."),
            "e1": _t("Eyes / nose / mouth", "आँख / नाक / मुँह", "ಕಣ್ಣು / ಮೂಗು / ಬಾಯಿ"),
            "e1e": _t("Splash exposure can infect through mucous membranes.", "छींटे से श्लेष्मा झिल्ली के माध्यम से संक्रमण हो सकता है।", "ಚಿಮ್ಮು ಸಂಪರ್ಕ ಶ್ಲೇಷ್ಮ ಪೊರೆಯ ಮೂಲಕ ಸೋಂಕುಗೊಳಿಸಬಹುದು."),
            "o0": _t("Kidneys", "गुर्दे", "ಮೂತ್ರಪಿಂಡಗಳು"),
            "o0e": _t("Leptospirosis can cause kidney injury in severe cases.", "गंभीर मामलों में लेप्टोस्पाइरोसिस गुर्दे को नुकसान पहुँचा सकता है।", "ಗಂಭೀರ ಪ್ರಕರಣಗಳಲ್ಲಿ ಲೆಪ್ಟೋಸ್ಪೈರೋಸಿಸ್ ಮೂತ್ರಪಿಂಡಕ್ಕೆ ಹಾನಿ ಉಂಟುಮಾಡಬಹುದು."),
            "o1": _t("Liver", "यकृत", "ಯಕೃತ್ತು"),
            "o1e": _t("Can lead to jaundice and weakness.", "पीलिया और कमज़ोरी का कारण बन सकता है।", "ಕಾಮಾಲೆ ಮತ್ತು ದುರ್ಬಲತೆಗೆ ಕಾರಣವಾಗಬಹುದು."),
        },
        "btb": {
            "r0": _t("Infected cow (Mycobacterium bovis)", "संक्रमित गाय (माइकोबैक्टीरियम बोविस)", "ಸೋಂಕಿತ ಹಸು (ಮೈಕೋಬ್ಯಾಕ್ಟೀರಿಯಂ ಬೋವಿಸ್)"),
            "r0e": _t("Bovine TB can spread via air and raw milk in some settings.", "कुछ परिस्थितियों में गाय का टीबी हवा और कच्चे दूध से फैल सकता है।", "ಕೆಲವು ಸಂದರ್ಭಗಳಲ್ಲಿ ಹಸುವಿನ ಟಿಬಿ ಗಾಳಿ ಮತ್ತು ಕಚ್ಚಾ ಹಾಲಿನ ಮೂಲಕ ಹರಡಬಹುದು."),
            "t0": _t("Airborne droplets near cow", "गाय के पास हवा में बूँदें", "ಹಸುವಿನ ಹತ್ತಿರ ವಾಯುವಿನ ಹನಿಗಳು"),
            "t0e": _t("Prolonged close contact can increase inhalation risk.", "लंबे समय निकट संपर्क से साँस लेने का जोखिम बढ़ सकता है।", "ದೀರ್ಘಕಾಲದ ಹತ್ತಿರದ ಸಂಪರ್ಕ ಉಸಿರಾಟದ ಅಪಾಯವನ್ನು ಹೆಚ್ಚಿಸಬಹುದು."),
            "t1": _t("Drinking raw milk", "कच्चा दूध पीना", "ಕಚ್ಚಾ ಹಾಲು ಕುಡಿಯುವುದು"),
            "t1e": _t("Unpasteurised milk can carry Mycobacterium bovis.", "बिना पाश्चुरीकृत दूध में माइकोबैक्टीरियम बोविस हो सकता है।", "ಪಾಸ್ಚರೀಕರಿಸದ ಹಾಲಿನಲ್ಲಿ ಮೈಕೋಬ್ಯಾಕ್ಟೀರಿಯಂ ಬೋವಿಸ್ ಇರಬಹುದು."),
            "e0": _t("Lungs (inhalation)", "फेफड़े (साँस)", "ಶ್ವಾಸಕೋಶಗಳು (ಉಸಿರಾಟ)"),
            "e0e": _t("Breathing contaminated droplets can seed infection in lungs.", "दूषित बूँदें साँस लेने से फेफड़ों में संक्रमण शुरू हो सकता है।", "ಕಲುಷಿತ ಹನಿಗಳನ್ನು ಉಸಿರಾಡುವುದು ಶ್ವಾಸಕೋಶಗಳಲ್ಲಿ ಸೋಂಕನ್ನು ಪ್ರಾರಂಭಿಸಬಹುದು."),
            "e1": _t("Mouth (ingestion)", "मुँह (निगलना)", "ಬಾಯಿ (ನುಂಗುವುದು)"),
            "e1e": _t("Raw milk exposure can affect gut and lymph nodes.", "कच्चे दूध के संपर्क से आंत और लसीका ग्रंथि प्रभावित हो सकते हैं।", "ಕಚ್ಚಾ ಹಾಲಿನ ಸಂಪರ್ಕ ಕರುಳು ಮತ್ತು ಲಸಿಕಾ ಗ್ರಂಥಿಗಳನ್ನು ಬಾಧಿಸಬಹುದು."),
            "o0": _t("Lungs", "फेफड़े", "ಶ್ವಾಸಕೋಶಗಳು"),
            "o0e": _t("Chronic cough and weight loss may occur over time.", "समय के साथ लंबी खाँसी और वजन घट सकता है।", "ಕಾಲಕ್ರಮೇಣ ದೀರ್ಘಕಾಲದ ಕೆಮ್ಮು ಮತ್ತು ತೂಕ ಇಳಿಕೆ ಸಂಭವಿಸಬಹುದು."),
            "o1": _t("Lymph nodes", "लसीका ग्रंथि", "ಲಸಿಕಾ ಗ್ರಂಥಿಗಳು"),
            "o1e": _t("Swollen nodes can be part of TB spread.", "सूजे ग्रंथि टीबी फैलने का हिस्सा हो सकते हैं।", "ಊತವಾದ ಗ್ರಂಥಿಗಳು ಟಿಬಿ ಪ್ರಸರಣದ ಭಾಗವಾಗಿರಬಹುದು."),
        },
        "anthrax": {
            "r0": _t("Carcass / infected tissue (Anthrax spores)", "शव / संक्रमित ऊतक (एंथ्रेक्स बीजाणु)", "ಶವ / ಸೋಂಕಿತ ಅಂಗಾಂಶ (ಆಂಥ್ರಾಕ್ಸ್ ಬೀಜಾಣುಗಳು)"),
            "r0e": _t("Spores can persist in soil and on animal tissue.", "बीजाणु मिट्टी और पशु ऊतक पर टिके रह सकते हैं।", "ಬೀಜಾಣುಗಳು ಮಣ್ಣಿನಲ್ಲಿ ಮತ್ತು ಪ್ರಾಣಿ ಅಂಗಾಂಶದಲ್ಲಿ ಉಳಿಯಬಹುದು."),
            "t0": _t("Skin contact with carcass/tissue", "शव/ऊतक से त्वचा संपर्क", "ಶವ/ಅಂಗಾಂಶದೊಂದಿಗೆ ಚರ್ಮ ಸಂಪರ್ಕ"),
            "t0e": _t("Handling carcasses without protection is very risky.", "बिना सुरक्षा शव छूना बहुत जोखिम भरा है।", "ರಕ್ಷಣೆಯಿಲ್ಲದೆ ಶವಗಳನ್ನು ನಿರ್ವಹಿಸುವುದು ಅತ್ಯಂತ ಅಪಾಯಕಾರಿ."),
            "t1": _t("Inhaling spores near carcass", "शव के पास बीजाणु साँस में लेना", "ಶವದ ಹತ್ತಿರ ಬೀಜಾಣುಗಳನ್ನು ಉಸಿರಾಡುವುದು"),
            "t1e": _t("Inhalation anthrax is rare but extremely dangerous.", "साँस से एंथ्रेक्स दुर्लभ लेकिन अत्यंत खतरनाक है।", "ಉಸಿರಾಟದ ಆಂಥ್ರಾಕ್ಸ್ ಅಪರೂಪ ಆದರೆ ಅತ್ಯಂತ ಅಪಾಯಕಾರಿ."),
            "e0": _t("Open skin wounds", "खुले त्वचा घाव", "ತೆರೆದ ಚರ್ಮದ ಗಾಯಗಳು"),
            "e0e": _t("Spores enter through cuts causing skin lesions.", "बीजाणु कट से प्रवेश कर त्वचा घाव बनाते हैं।", "ಬೀಜಾಣುಗಳು ಕತ್ತರಿಸುವಿಕೆಯ ಮೂಲಕ ಪ್ರವೇಶಿಸಿ ಚರ್ಮದ ಗಾಯಗಳನ್ನು ಉಂಟುಮಾಡುತ್ತವೆ."),
            "e1": _t("Lungs (inhalation)", "फेफड़े (साँस)", "ಶ್ವಾಸಕೋಶಗಳು (ಉಸಿರಾಟ)"),
            "e1e": _t("Breathing spores can cause severe respiratory illness.", "बीजाणु साँस लेने से गंभीर श्वसन रोग हो सकता है।", "ಬೀಜಾಣುಗಳನ್ನು ಉಸಿರಾಡುವುದು ಗಂಭೀರ ಉಸಿರಾಟದ ಅನಾರೋಗ್ಯಕ್ಕೆ ಕಾರಣವಾಗಬಹುದು."),
            "o0": _t("Bloodstream", "रक्तप्रवाह", "ರಕ್ತನಾಳ"),
            "o0e": _t("Can progress rapidly and become life-threatening.", "तेज़ी से बढ़कर जानलेवा हो सकता है।", "ವೇಗವಾಗಿ ಹರಡಿ ಜೀವಕ್ಕೆ ಅಪಾಯವಾಗಬಹುದು."),
            "o1": _t("Lungs", "फेफड़े", "ಶ್ವಾಸಕೋಶಗಳು"),
            "o1e": _t("Severe breathing difficulty can occur with inhalation exposure.", "साँस से संपर्क में गंभीर साँस की तकलीफ हो सकती है।", "ಉಸಿರಾಟದ ಸಂಪರ್ಕದಲ್ಲಿ ಗಂಭೀರ ಉಸಿರಾಟದ ತೊಂದರೆ ಸಂಭವಿಸಬಹುದು."),
        },
        "qfever": {
            "r0": _t("Infected cow (Coxiella burnetii)", "संक्रमित गाय (कॉक्सिएला बर्नेटी)", "ಸೋಂಕಿತ ಹಸು (ಕಾಕ್ಸಿಯೆಲ್ಲಾ ಬರ್ನೆಟೀ)"),
            "r0e": _t("Bacteria may be present in birth fluids and dust around animals.", "जानवरों के आसपास प्रसव द्रव और धूल में बैक्टीरिया हो सकता है।", "ಪ್ರಾಣಿಗಳ ಸುತ್ತ ಜನನ ದ್ರವ ಮತ್ತು ಧೂಳಿನಲ್ಲಿ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಇರಬಹುದು."),
            "t0": _t("Inhaling contaminated dust", "दूषित धूल साँस में लेना", "ಕಲುಷಿತ ಧೂಳನ್ನು ಉಸಿರಾಡುವುದು"),
            "t0e": _t("Dust from birth fluids can carry bacteria into air.", "प्रसव द्रव की धूल हवा में बैक्टीरिया ले जा सकती है।", "ಜನನ ದ್ರವದ ಧೂಳು ಗಾಳಿಯಲ್ಲಿ ಬ್ಯಾಕ್ಟೀರಿಯಾವನ್ನು ಹೊತ್ತು ಹೋಗಬಹುದು."),
            "t1": _t("Raw milk consumption", "कच्चा दूध पीना", "ಕಚ್ಚಾ ಹಾಲು ಸೇವನೆ"),
            "t1e": _t("Raw milk may carry bacteria; pasteurisation reduces risk.", "कच्चे दूध में बैक्टीरिया हो सकता है; पाश्चुरीकरण जोखिम कम करता है।", "ಕಚ್ಚಾ ಹಾಲಿನಲ್ಲಿ ಬ್ಯಾಕ್ಟೀರಿಯಾ ಇರಬಹುದು; ಪಾಸ್ಚರೀಕರಣ ಅಪಾಯವನ್ನು ಕಡಿಮೆ ಮಾಡುತ್ತದೆ."),
            "e0": _t("Lungs (inhalation)", "फेफड़े (साँस)", "ಶ್ವಾಸಕೋಶಗಳು (ಉಸಿರಾಟ)"),
            "e0e": _t("Inhalation is a main route for Q fever infection.", "साँस लेना क्यू बुखार संक्रमण का मुख्य मार्ग है।", "ಉಸಿರಾಡುವುದು ಕ್ಯೂ ಜ್ವರ ಸೋಂಕಿನ ಪ್ರಮುಖ ಮಾರ್ಗ."),
            "e1": _t("Mouth (ingestion)", "मुँह (निगलना)", "ಬಾಯಿ (ನುಂಗುವುದು)"),
            "e1e": _t("Ingestion is a secondary route.", "निगलना द्वितीयक मार्ग है।", "ನುಂಗುವುದು ದ್ವಿತೀಯ ಮಾರ್ಗ."),
            "o0": _t("Lungs", "फेफड़े", "ಶ್ವಾಸಕೋಶಗಳು"),
            "o0e": _t("May cause flu-like illness and pneumonia.", "फ़्लू जैसी बीमारी और निमोनिया हो सकता है।", "ಜ್ವರದಂತೆ ಅನಾರೋಗ್ಯ ಮತ್ತು ನ್ಯುಮೋನಿಯಾ ಉಂಟಾಗಬಹುದು."),
            "o1": _t("Heart (rare)", "हृदय (दुर्लभ)", "ಹೃದಯ (ಅಪರೂಪ)"),
            "o1e": _t("Chronic Q fever can affect heart valves in rare cases.", "दुर्लभ मामलों में पुराना क्यू बुखार हृदय वाल्व को प्रभावित कर सकता है।", "ಅಪರೂಪದ ಪ್ರಕರಣಗಳಲ್ಲಿ ದೀರ್ಘಕಾಲದ ಕ್ಯೂ ಜ್ವರ ಹೃದಯ ಕವಾಟಗಳನ್ನು ಬಾಧಿಸಬಹುದು."),
        },
        "lsd": {
            "r0": _t("Infected cow (LSD virus)", "संक्रमित गाय (एलएसडी वायरस)", "ಸೋಂಕಿತ ಹಸು (ಎಲ್ಎಸ್ಡಿ ವೈರಸ್)"),
            "r0e": _t("LSD is mainly an animal disease; human infection is not expected.", "एलएसडी मुख्यतः पशु रोग है; मानव संक्रमण की अपेक्षा नहीं।", "ಎಲ್ಎಸ್ಡಿ ಮುಖ್ಯವಾಗಿ ಪ್ರಾಣಿ ರೋಗ; ಮಾನವ ಸೋಂಕು ನಿರೀಕ್ಷಿಸಲಾಗುವುದಿಲ್ಲ."),
            "t0": _t("Not directly transmissible to humans", "मनुष्यों में सीधे संक्रामक नहीं", "ಮಾನವರಿಗೆ ನೇರವಾಗಿ ಹರಡುವುದಿಲ್ಲ"),
            "t0e": _t("Human risk is extremely low based on current evidence.", "वर्तमान साक्ष्य के अनुसार मानव जोखिम बहुत कम है।", "ಪ್ರಸ್ತುತ ಪುರಾವೆಗಳ ಆಧಾರದ ಮೇಲೆ ಮಾನವ ಅಪಾಯ ಅತ್ಯಂತ ಕಡಿಮೆ."),
            "t1": _t("Vector bite (rare)", "वेक्टर काटना (दुर्लभ)", "ವೆಕ್ಟರ್ ಕಚ್ಚುವುದು (ಅಪರೂಪ)"),
            "t1e": _t("Insects can spread among animals; human risk remains very low.", "कीट पशुओं में फैला सकते हैं; मानव जोखिम बहुत कम रहता है।", "ಕೀಟಗಳು ಪ್ರಾಣಿಗಳ ನಡುವೆ ಹರಡಬಹುದು; ಮಾನವ ಅಪಾಯ ಬಹು ಕಡಿಮೆ."),
            "e0": _t("—", "—", "—"),
            "e0e": _t("No common human entry route is established.", "कोई सामान्य मानव प्रवेश मार्ग स्थापित नहीं।", "ಯಾವುದೇ ಸಾಮಾನ್ಯ ಮಾನವ ಪ್ರವೇಶ ಮಾರ್ಗ ಸ್ಥಾಪಿತವಾಗಿಲ್ಲ."),
            "o0": _t("—", "—", "—"),
            "o0e": _t("No known human target organs for LSD.", "एलएसडी के लिए कोई ज्ञात मानव लक्ष्य अंग नहीं।", "ಎಲ್ಎಸ್ಡಿಗೆ ತಿಳಿದ ಮಾನವ ಗುರಿ ಅಂಗಗಳಿಲ್ಲ."),
        },
        "fmd": {
            "r0": _t("Infected cow (FMD virus)", "संक्रमित गाय (एफएमडी वायरस)", "ಸೋಂಕಿತ ಹಸು (ಎಫ್ಎಂಡಿ ವೈರಸ್)"),
            "r0e": _t("FMD is mostly an animal disease; humans are rarely affected.", "एफएमडी ज्यादातर पशु रोग है; मनुष्य शायद ही प्रभावित होते हैं।", "ಎಫ್ಎಂಡಿ ಹೆಚ್ಚಾಗಿ ಪ್ರಾಣಿ ರೋಗ; ಮಾನವರು ಅಪರೂಪವಾಗಿ ಬಾಧಿತರಾಗುತ್ತಾರೆ."),
            "t0": _t("Direct contact with blisters/saliva", "फफोले/लार से सीधा संपर्क", "ಗುಳ್ಳೆಗಳು/ಲಾಲಾರಸದ ನೇರ ಸಂಪರ್ಕ"),
            "t0e": _t("Handling lesions without protection can increase risk.", "बिना सुरक्षा घाव छूने से जोखिम बढ़ सकता है।", "ರಕ್ಷಣೆಯಿಲ್ಲದೆ ಗಾಯಗಳನ್ನು ನಿರ್ವಹಿಸುವುದು ಅಪಾಯವನ್ನು ಹೆಚ್ಚಿಸಬಹುದು."),
            "t1": _t("Raw milk from infected cow", "संक्रमित गाय का कच्चा दूध", "ಸೋಂಕಿತ ಹಸುವಿನ ಕಚ್ಚಾ ಹಾಲು"),
            "t1e": _t("Raw milk can carry virus; pasteurisation reduces risk.", "कच्चे दूध में वायरस हो सकता है; पाश्चुरीकरण जोखिम कम करता है।", "ಕಚ್ಚಾ ಹಾಲಿನಲ್ಲಿ ವೈರಸ್ ಇರಬಹುದು; ಪಾಸ್ಚರೀಕರಣ ಅಪಾಯ ಕಡಿಮೆ ಮಾಡುತ್ತದೆ."),
            "e0": _t("Mouth (ingestion)", "मुँह (निगलना)", "ಬಾಯಿ (ನುಂಗುವುದು)"),
            "e0e": _t("Consumption of raw milk is a potential route.", "कच्चा दूध पीना संभावित मार्ग है।", "ಕಚ್ಚಾ ಹಾಲು ಸೇವನೆ ಸಂಭಾವ್ಯ ಮಾರ್ಗ."),
            "e1": _t("Skin contact", "त्वचा संपर्क", "ಚರ್ಮ ಸಂಪರ್ಕ"),
            "e1e": _t("Contact with lesions can cause rare human infection.", "घाव के संपर्क से दुर्लभ मानव संक्रमण हो सकता है।", "ಗಾಯಗಳ ಸಂಪರ್ಕದಿಂದ ಅಪರೂಪದ ಮಾನವ ಸೋಂಕು ಸಂಭವಿಸಬಹುದು."),
            "o0": _t("Skin / mouth", "त्वचा / मुँह", "ಚರ್ಮ / ಬಾಯಿ"),
            "o0e": _t("Rarely causes mild lesions in humans.", "मनुष्यों में शायद ही हल्के घाव होते हैं।", "ಮಾನವರಲ್ಲಿ ಅಪರೂಪವಾಗಿ ಸೌಮ್ಯ ಗಾಯಗಳನ್ನು ಉಂಟುಮಾಡುತ್ತದೆ."),
        },
        "ring": {
            "r0": _t("Infected cow (fungal spores)", "संक्रमित गाय (फंगल बीजाणु)", "ಸೋಂಕಿತ ಹಸು (ಶಿಲೀಂಧ್ರ ಬೀಜಾಣುಗಳು)"),
            "r0e": _t("Ringworm spreads via spores on skin and hair.", "दाद त्वचा और बाल पर बीजाणु से फैलता है।", "ಬಳಪ ಚರ್ಮ ಮತ್ತು ಕೂದಲಿನಲ್ಲಿನ ಬೀಜಾಣುಗಳ ಮೂಲಕ ಹರಡುತ್ತದೆ."),
            "t0": _t("Direct skin contact", "सीधा त्वचा संपर्क", "ನೇರ ಚರ್ಮ ಸಂಪರ್ಕ"),
            "t0e": _t("Touching infected areas can transfer spores to humans.", "संक्रमित क्षेत्र छूने से बीजाणु मनुष्यों को लग सकते हैं।", "ಸೋಂಕಿತ ಪ್ರದೇಶಗಳನ್ನು ಮುಟ್ಟುವುದು ಬೀಜಾಣುಗಳನ್ನು ಮಾನವರಿಗೆ ವರ್ಗಾಯಿಸಬಹುದು."),
            "t1": _t("Contaminated bedding/equipment", "दूषित बिस्तर/उपकरण", "ಕಲುಷಿತ ಹಾಸು/ಉಪಕರಣಗಳು"),
            "t1e": _t("Spores survive on surfaces; shared tools can spread infection.", "बीजाणु सतह पर जीवित रहते हैं; साझा उपकरण संक्रमण फैला सकते हैं।", "ಬೀಜಾಣುಗಳು ಮೇಲ್ಮೈಯಲ್ಲಿ ಉಳಿಯುತ್ತವೆ; ಹಂಚಿಕೊಂಡ ಸಾಧನಗಳು ಸೋಂಕು ಹರಡಬಹುದು."),
            "e0": _t("Skin (micro-cuts)", "त्वचा (सूक्ष्म कट)", "ಚರ್ಮ (ಸೂಕ್ಷ್ಮ ಕತ್ತರಿಸುವಿಕೆ)"),
            "e0e": _t("Spores enter through tiny skin breaks and cause itchy patches.", "बीजाणु छोटे कट से प्रवेश कर खुजली वाले धब्बे बनाते हैं।", "ಬೀಜಾಣುಗಳು ಸಣ್ಣ ಚರ್ಮ ಬಿರುಕುಗಳ ಮೂಲಕ ಪ್ರವೇಶಿಸಿ ನುರಿತ ಪ್ಯಾಚ್‌ಗಳನ್ನು ಉಂಟುಮಾಡುತ್ತವೆ."),
            "o0": _t("Skin", "त्वचा", "ಚರ್ಮ"),
            "o0e": _t("Usually causes circular itchy rashes on skin.", "आमतौर पर त्वचा पर गोल खुजली वाले दाने होते हैं।", "ಸಾಮಾನ್ಯವಾಗಿ ಚರ್ಮದಲ್ಲಿ ವೃತ್ತಾಕಾರ ನುರಿತ ಚರ್ಮದ ಪೊಕ್ಕುಗಳನ್ನು ಉಂಟುಮಾಡುತ್ತದೆ."),
        },
    }
    nodes.update(packs)
    for prefix, pack in nodes.items():
        for k, v in pack.items():
            out[f"path_{prefix}_{k}"] = v
    return out


def route_entries() -> dict[str, dict[str, str]]:
    return {
        "route_bruc_primary": _t("Raw milk or unpasteurised dairy", "कच्चा दूध या बिना पाश्चुरीकृत डेयरी", "ಕಚ್ಚಾ ಹಾಲು ಅಥವಾ ಪಾಸ್ಚರೀಕರಿಸದ ಡೈರಿ"),
        "route_bruc_secondary": _t("Contact with birth fluids or aborted fetuses", "प्रसव द्रव या गर्भपात संपर्क", "ಜನನ ದ್ರವ ಅಥವಾ ಗರ್ಭಪಾತ ಸಂಪರ್ಕ"),
        "route_lepto_primary": _t("Contact with urine-contaminated water or soil", "मूत्र-दूषित पानी या मिट्टी संपर्क", "ಮೂತ್ರ-ಕಲುಷಿತ ನೀರು ಅಥವಾ ಮಣ್ಣು ಸಂಪರ್ಕ"),
        "route_lepto_secondary": _t("Open wound contact with infected tissue", "संक्रमित ऊतक से खुले घाव का संपर्क", "ಸೋಂಕಿತ ಅಂಗಾಂಶದೊಂದಿಗೆ ತೆರೆದ ಗಾಯ ಸಂಪರ್ಕ"),
        "route_btb_primary": _t("Inhaling airborne droplets near infected cow", "संक्रमित गाय के पास हवा की बूँदें साँस में लेना", "ಸೋಂಕಿತ ಹಸುವಿನ ಹತ್ತಿರ ಗಾಳಿಯ ಹನಿಗಳನ್ನು ಉಸಿರಾಡುವುದು"),
        "route_btb_secondary": _t("Drinking raw milk", "कच्चा दूध पीना", "ಕಚ್ಚಾ ಹಾಲು ಕುಡಿಯುವುದು"),
        "route_anthrax_primary": _t("Skin contact with infected animal tissue or carcass", "संक्रमित ऊतक या शव से त्वचा संपर्क", "ಸೋಂಕಿತ ಅಂಗಾಂಶ ಅಥವಾ ಶವದೊಂದಿಗೆ ಚರ್ಮ ಸಂಪರ್ಕ"),
        "route_anthrax_secondary": _t("Inhaling spores near a carcass", "शव के पास बीजाणु साँस में लेना", "ಶವದ ಹತ್ತಿರ ಬೀಜಾಣುಗಳನ್ನು ಉಸಿರಾಡುವುದು"),
        "route_qfever_primary": _t("Inhaling dust or particles from birth fluids", "प्रसव द्रव की धूल या कण साँस में लेना", "ಜನನ ದ್ರವದ ಧೂಳು ಅಥವಾ ಕಣಗಳನ್ನು ಉಸಿರಾಡುವುದು"),
        "route_qfever_secondary": _t("Raw milk consumption", "कच्चा दूध पीना", "ಕಚ್ಚಾ ಹಾಲು ಸೇವನೆ"),
        "route_lsd_primary": _t("Not directly transmissible to humans", "मनुष्यों में सीधे संक्रामक नहीं", "ಮಾನವರಿಗೆ ನೇರವಾಗಿ ಹರಡುವುದಿಲ್ಲ"),
        "route_lsd_secondary": _t("Insect bite from vector on infected cow (rare)", "संक्रमित गाय पर कीट काटना (दुर्लभ)", "ಸೋಂಕಿತ ಹಸುವಿನ ಕೀಟ ಕಚ್ಚುವುದು (ಅಪರೂಪ)"),
        "route_fmd_primary": _t("Direct contact with blisters or saliva", "फफोले या लार से सीधा संपर्क", "ಗುಳ್ಳೆಗಳು ಅಥವಾ ಲಾಲಾರಸದ ನೇರ ಸಂಪರ್ಕ"),
        "route_fmd_secondary": _t("Raw milk from infected cow", "संक्रमित गाय का कच्चा दूध", "ಸೋಂಕಿತ ಹಸುವಿನ ಕಚ್ಚಾ ಹಾಲು"),
        "route_ring_primary": _t("Direct skin contact with infected animal", "संक्रमित पशु से सीधा त्वचा संपर्क", "ಸೋಂಕಿತ ಪ್ರಾಣಿಯೊಂದಿಗೆ ನೇರ ಚರ್ಮ ಸಂಪರ್ಕ"),
        "route_ring_secondary": _t("Contact with contaminated bedding or equipment", "दूषित बिस्तर या उपकरण संपर्क", "ಕಲುಷಿತ ಹಾಸು ಅಥವಾ ಉಪಕರಣ ಸಂಪರ್ಕ"),
    }


def group_entries() -> dict[str, dict[str, str]]:
    return {
        "group_pregnant_women": _t("Pregnant women", "गर्भवती महिलाएँ", "ಗರ್ಭಿಣಿ ಮಹಿಳೆಯರು"),
        "group_pregnant_miscarriage": _t("Pregnant women (risk of miscarriage)", "गर्भवती महिलाएँ (गर्भपात का जोखिम)", "ಗರ್ಭಿಣಿ ಮಹಿಳೆಯರು (ಗರ್ಭಪಾತದ ಅಪಾಯ)"),
        "group_children_under_10": _t("Children under 10", "10 वर्ष से कम बच्चे", "10 ವರ್ಷಕ್ಕಿಂತ ಕಡಿಮೆ ಮಕ್ಕಳು"),
        "group_children_under_5": _t("Children under 5", "5 वर्ष से कम बच्चे", "5 ವರ್ಷಕ್ಕಿಂತ ಕಡಿಮೆ ಮಕ್ಕಳು"),
        "group_elderly": _t("Elderly", "बुजुर्ग", "ವೃದ್ಧರು"),
        "group_immunocompromised": _t("Immunocompromised individuals", "कमज़ोर प्रतिरक्षा वाले", "ರೋಗಪ್ರತಿರೋಧಕ ಶಕ್ತಿ ಕಡಿಮೆಯವರು"),
        "group_open_wounds": _t("Anyone with open wounds", "खुले घाव वाले कोई भी", "ತೆರೆದ ಗಾಯಗಳಿರುವ ಯಾರಾದರೂ"),
        "group_open_wounds_cuts": _t("Anyone with open wounds or cuts", "खुले घाव या कट वाले कोई भी", "ತೆರೆದ ಗಾಯಗಳು ಅಥವಾ ಕತ್ತರಿಸುವಿಕೆಗಳಿರುವ ಯಾರಾದರೂ"),
        "group_farmers_water": _t("Farmers wading in water", "पानी में उतरने वाले किसान", "ನೀರಿನಲ್ಲಿ ನಡೆಯುವ ರೈತರು"),
    }


def watch_symptom_entries() -> dict[str, dict[str, str]]:
    return {
        "watch_fever": _t("Fever", "बुखार", "ಜ್ವರ"),
        "watch_joint_pain": _t("Joint pain", "जोड़ों का दर्द", "ಕೀಲು ನೋವು"),
        "watch_night_sweats": _t("Night sweats", "रात को पसीना", "ರಾತ್ರಿ ಬೆವರು"),
        "watch_fatigue": _t("Fatigue", "थकान", "ಅಲಸತೆ"),
        "watch_loss_appetite": _t("Loss of appetite", "भूख न लगना", "ಆಹಾರ ಇಷ್ಟವಿಲ್ಲದಿರುವುದು"),
        "watch_high_fever": _t("High fever", "तेज़ बुखार", "ಅಧಿಕ ಜ್ವರ"),
        "watch_severe_headache": _t("Severe headache", "गंभीर सिरदर्द", "ತೀವ್ರ ತಲೆನೋವು"),
        "watch_muscle_aches": _t("Muscle aches", "मांसपेशियों में दर्द", "ಸ್ನಾಯು ನೋವು"),
        "watch_red_eyes": _t("Red eyes", "लाल आँखें", "ಕೆಂಪು ಕಣ್ಣುಗಳು"),
        "watch_jaundice": _t("Jaundice", "पीलिया", "ಕಾಮಾಲೆ"),
        "watch_persistent_cough": _t("Persistent cough (3+ weeks)", "लगातार खाँसी (3+ सप्ताह)", "ನಿರಂತರ ಕೆಮ್ಮು (3+ ವಾರಗಳು)"),
        "watch_weight_loss": _t("Unexplained weight loss", "अकारण वजन घटना", "ವಿವರಣೆಯಿಲ್ಲದ ತೂಕ ಇಳಿಕೆ"),
        "watch_chest_pain": _t("Chest pain", "सीने में दर्द", "ಛಾತಿಯ ನೋವು"),
        "watch_black_sore": _t("Black skin sore (painless)", "काला त्वचा घाव (दर्द रहित)", "ಕಪ್ಪು ಚರ್ಮದ ಗಾಯ (ನೋವಿಲ್ಲದ)"),
        "watch_swollen_nodes": _t("Swollen lymph nodes", "सूजे लसीका ग्रंथि", "ಊತವಾದ ಲಸಿಕಾ ಗ್ರಂಥಿಗಳು"),
        "watch_difficulty_breathing": _t("Difficulty breathing", "साँस लेने में कठिनाई", "ಉಸಿರಾಟದ ತೊಂದರೆ"),
        "watch_sudden_high_fever": _t("Sudden high fever", "अचानक तेज़ बुखार", "ಅಚಾನಕ ಅಧಿಕ ಜ್ವರ"),
        "watch_severe_fatigue": _t("Severe fatigue", "गंभीर थकान", "ತೀವ್ರ ಅಲಸತೆ"),
        "watch_muscle_pain": _t("Muscle pain", "मांसपेशी दर्द", "ಸ್ನಾಯು ನೋವು"),
        "watch_blisters_mouth": _t("Blisters in mouth", "मुँह में फफोले", "ಬಾಯಿಯಲ್ಲಿ ಗುಳ್ಳೆಗಳು"),
        "watch_blisters_hands_feet": _t("Blisters on hands and feet", "हाथ-पैर पर फफोले", "ಕೈ-ಕಾಲುಗಳಲ್ಲಿ ಗುಳ್ಳೆಗಳು"),
        "watch_skin_nodules": _t("Skin nodules", "त्वचा पर गांठें", "ಚರ್ಮದ ಗುಂಡಿಗಳು"),
        "watch_nasal_discharge": _t("Nasal discharge", "नाक से स्राव", "ಮೂಗಿನ ಸ್ರಾವ"),
        "watch_circular_rash": _t("Circular itchy rash", "गोल खुजली वाला दाने", "ವೃತ್ತಾಕಾರ ನುರಿತ ಚರ್ಮದ ಪೊಕ್ಕು"),
        "watch_scaly_patch": _t("Scaly skin patch", "खुरदरी त्वचा का धब्बा", "ಒರಟು ಚರ್ಮದ ಪ್ಯಾಚ್"),
        "watch_hair_loss": _t("Hair loss in affected area", "प्रभावित क्षेत्र में बाल झड़ना", "ಬಾಧಿತ ಪ್ರದೇಶದಲ್ಲಿ ಕೂದಲು ಉದುರಿಸುವಿಕೆ"),
        "watch_worsening_fever": _t("Worsening fever or weakness", "बढ़ता बुखार या कमज़ोरी", "ಹೆಚ್ಚುತ್ತಿರುವ ಜ್ವರ ಅಥವಾ ದುರ್ಬಲತೆ"),
        "watch_refusing_feed": _t("Refusing feed or water", "चारा या पानी न लेना", "ಆಹಾರ ಅಥವಾ ನೀರು ತೆಗೆದುಕೊಳ್ಳದಿರುವುದು"),
        "watch_new_breathing": _t("New breathing difficulty", "नई साँस की तकलीफ", "ಹೊಸ ಉಸಿರಾಟದ ತೊಂದರೆ"),
        "watch_new_bleeding": _t("New bleeding or discharge", "नया खून बहना या स्राव", "ಹೊಸ ರಕ್ತಸ್ರಾವ ಅಥವಾ ಸ್ರಾವ"),
        "watch_behaviour_change": _t("Sudden behaviour change", "अचानक व्यवहार बदलाव", "ಅಚಾನಕ ವರ್ತನೆ ಬದಲಾವಣೆ"),
    }


def guidance_entries() -> dict[str, dict[str, str]]:
    g = {}
    data = {
        "bruc": {
            "immediate": ("Isolate the animal from the rest of the herd immediately.", "पशु को तुरंत झुंड से अलग करें।", "ಜಾನುವಾರನ್ನು ತಕ್ಷಣ ಕೂಪದಿಂದ ಪ್ರತ್ಯೇಕಿಸಿ."),
            "do_not": ("Do not allow the animal to breed. Do not consume its milk until tested.", "प्रजनन न करने दें। जाँच तक दूध न पिएँ।", "ಸಂತಾನೋತ್ಪತ್ತಿಗೆ ಅನುಮತಿಸಬೇಡಿ. ಪರೀಕ್ಷೆ ವರೆಗೆ ಹಾಲು ಸೇವಿಸಬೇಡಿ."),
            "vet_action": ("Request a Rose Bengal Plate Test (RBPT) from a government vet.", "सरकारी पशु चिकित्सक से आरबीपीटी परीक्षण कराएँ।", "ಸರ್ಕಾರಿ ಪಶುವೈದ್ಯರಿಂದ ಆರ್‌ಬಿಪಿಟಿ ಪರೀಕ್ಷೆ ಮಾಡಿಸಿ."),
            "recovery": ("Brucellosis has no cure in cattle. If confirmed, the animal may need to be culled per government protocol.", "गाय में ब्रूसेलोसिस का इलाज नहीं। पुष्टि पर सरकारी प्रोटोकॉल के अनुसार मारा जा सकता है।", "ಹಸುಗಳಲ್ಲಿ ಬ್ರೂಸೆಲ್ಲೋಸಿಸ್‌ಗೆ ಗುಣಪಡಿಸುವಿಕೆ ಇಲ್ಲ. ದೃಢೀಕರಣದ ನಂತರ ಸರ್ಕಾರಿ ಪ್ರೋಟೋಕಾಲ್ ಪ್ರಕಾರ ಮಾರಬೇಕಾಗಬಹುದು."),
        },
        "lepto": {
            "immediate": ("Keep the animal away from water sources and other cattle.", "पशु को पानी के स्रोत और अन्य पशुओं से दूर रखें।", "ಜಾನುವಾರನ್ನು ನೀರಿನ ಮೂಲಗಳು ಮತ್ತು ಇತರ ಹಸುಗಳಿಂದ ದೂರವಿಡಿ."),
            "do_not": ("Do not let the animal wade in common water troughs or ponds.", "साझा पानी में उतरने न दें।", "ಸಾಮಾನ್ಯ ನೀರಿನಲ್ಲಿ ನಡೆಯಲು ಬಿಡಬೇಡಿ."),
            "vet_action": ("A government vet can prescribe antibiotics (penicillin/streptomycin) — effective if caught early.", "सरकारी पशु चिकित्सक एंटीबायोटिक दे सकते हैं — जल्दी पकड़ने पर प्रभावी।", "ಸರ್ಕಾರಿ ಪಶುವೈದ್ಯರು ಆಂಟಿಬಯೋಟಿಕ್ ನೀಡಬಹುದು — ಬೇಗ ಪತ್ತೆಯಾದರೆ ಪರಿಣಾಮಕಾರಿ."),
            "recovery": ("Most cattle recover with antibiotic treatment within 1–2 weeks.", "अधिकांश पशु 1–2 सप्ताह में एंटीबायोटिक से ठीक हो जाते हैं।", "ಹೆಚ್ಚಿನ ಹಸುಗಳು 1–2 ವಾರಗಳಲ್ಲಿ ಆಂಟಿಬಯೋಟಿಕ್‌ನಿಂದ ಗುಣಮುಖವಾಗುತ್ತವೆ."),
        },
        "btb": {
            "immediate": ("Isolate the animal. Avoid close contact — especially in enclosed spaces.", "पशु को अलग करें। निकट संपर्क से बचें — खासकर बंद जगह में।", "ಜಾನುವಾರನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ. ಹತ್ತಿರದ ಸಂಪರ್ಕ ತಪ್ಪಿಸಿ — ವಿಶೇಷವಾಗಿ ಮುಚ್ಚಿದ ಸ್ಥಳಗಳಲ್ಲಿ."),
            "do_not": ("Do not sell or transport the animal. Do not consume raw milk.", "पशु बेचें या ले जाएँ नहीं। कच्चा दूध न पिएँ।", "ಜಾನುವಾರನ್ನು ಮಾರಬೇಡಿ ಅಥವಾ ಸಾಗಿಸಬೇಡಿ. ಕಚ್ಚಾ ಹಾಲು ಸೇವಿಸಬೇಡಿ."),
            "vet_action": ("Request a Tuberculin Skin Test (TST) from a government vet. Notify your district animal husbandry officer — bTB is notifiable.", "सरकारी पशु चिकित्सक से टीएसटी कराएँ। जिला पशुपालन अधिकारी को सूचित करें — बीटीबी सूचनात्मक रोग है।", "ಸರ್ಕಾರಿ ಪಶುವೈದ್ಯರಿಂದ ಟಿಎಸ್‌ಟಿ ಮಾಡಿಸಿ. ಜಿಲ್ಲಾ ಪಶುಸಂಗೋಪನೆ ಅಧಿಕಾರಿಗೆ ತಿಳಿಸಿ — ಬಿಟಿಬಿ ಸೂಚನೀಯ ರೋಗ."),
            "recovery": ("There is no approved treatment for bTB in cattle in India. Confirmed cases are typically culled under the National TB programme.", "भारत में गाय के बीटीबी का स्वीकृत इलाज नहीं। पुष्ट मामले आमतौर पर राष्ट्रीय टीबी कार्यक्रम के तहत मारे जाते हैं।", "ಭಾರತದಲ್ಲಿ ಹಸುವಿನ ಬಿಟಿಬಿಗೆ ಅನುಮೋದಿತ ಚಿಕಿತ್ಸೆ ಇಲ್ಲ. ದೃಢೀಕೃತ ಪ್ರಕರಣಗಳನ್ನು ಸಾಮಾನ್ಯವಾಗಿ ರಾಷ್ಟ್ರೀಯ ಟಿಬಿ ಕಾರ್ಯಕ್ರಮದಲ್ಲಿ ಮಾರಲಾಗುತ್ತದೆ."),
        },
        "anthrax": {
            "immediate": ("Do NOT move, open, or skin the carcass if the animal has died. Anthrax spores spread when a carcass is disturbed.", "पशु मरा हो तो शव न हिलाएँ, न खोलें, न छीलें। शव छेड़ने पर एंथ्रेक्स बीजाणु फैलते हैं।", "ಜಾನುವಾರು ಸತ್ತಿದ್ದರೆ ಶವವನ್ನು ಸರಿಸಬೇಡಿ, ತೆರೆಯಬೇಡಿ, ಚರ್ಮ ತೆಗೆಯಬೇಡಿ. ಶವಕ್ಕೆ ತೊಂದರೆ ಕೊಟ್ಟರೆ ಆಂಥ್ರಾಕ್ಸ್ ಬೀಜಾಣುಗಳು ಹರಡುತ್ತವೆ."),
            "do_not": ("Do not allow any person or other animal near the carcass. Do not consume any part of the animal.", "कोई भी व्यक्ति या पशु शव के पास न जाए। पशु का कोई भी हिस्सा न खाएँ।", "ಯಾರೂ ಅಥವಾ ಬೇರೆ ಪ್ರಾಣಿ ಶವದ ಹತ್ತಿರ ಹೋಗಲು ಬಿಡಬೇಡಿ. ಜಾನುವಾರಿನ ಯಾವುದೇ ಭಾಗವನ್ನು ಸೇವಿಸಬೇಡಿ."),
            "vet_action": ("Call the district veterinary officer immediately — Anthrax is a notifiable disease. Surviving animals can be vaccinated.", "तुरंत जिला पशु चिकित्सा अधिकारी को बुलाएँ — एंथ्रेक्स सूचनात्मक रोग है। बचे पशुओं का टीका लग सकता है।", "ತಕ್ಷಣ ಜಿಲ್ಲಾ ಪಶು ವೈದ್ಯಾಧಿಕಾರಿಯನ್ನು ಕರೆ ಮಾಡಿ — ಆಂಥ್ರಾಕ್ಸ್ ಸೂಚನೀಯ ರೋಗ. ಬದುಕಿದ ಪ್ರಾಣಿಗಳಿಗೆ ಲಸಿಕೆ ಹಾಕಬಹುದು."),
            "recovery": ("Anthrax in cattle is often fatal. If alive, high-dose penicillin may be administered by a vet.", "गाय में एंथ्रेक्स अक्सर घातक। जीवित हो तो पशु चिकित्सक उच्च खुराक पेनिसिलिन दे सकते हैं।", "ಹಸುಗಳಲ್ಲಿ ಆಂಥ್ರಾಕ್ಸ್ ಹೆಚ್ಚಾಗಿ ಮರಣಾಂತಿಕ. ಬದುಕಿದ್ದರೆ ಪಶುವೈದ್ಯರು ಹೆಚ್ಚಿನ ಮೋತಾದ ಪೆನಿಸಿಲಿನ್ ನೀಡಬಹುದು."),
        },
        "qfever": {
            "immediate": ("Isolate the animal, especially during and after birthing.", "पशु को अलग रखें, खासकर प्रसव के दौरान और बाद में।", "ಜಾನುವಾರನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ, ವಿಶೇಷವಾಗಿ ಜನನದ ಸಮಯ ಮತ್ತು ನಂತರ."),
            "do_not": ("Do not handle birth fluids, placenta, or aborted material without heavy gloves and a mask.", "भारी दस्ताने और मास्क के बिना प्रसव द्रव, प्लेसेंटा या गर्भपात सामग्री न छुएँ।", "ಭಾರೀ ಕೈಗವಸು ಮತ್ತು ಮುಖವಾಡವಿಲ್ಲದೆ ಜನನ ದ್ರವ, ಜರಾಯು ಅಥವಾ ಗರ್ಭಪಾತ ಸಾಮಗ್ರಿ ನಿರ್ವಹಿಸಬೇಡಿ."),
            "vet_action": ("A vet can prescribe tetracycline. Vaccination is available in some states.", "पशु चिकित्सक टेट्रासाइक्लिन दे सकते हैं। कुछ राज्यों में टीका उपलब्ध है।", "ಪಶುವೈದ್ಯರು ಟೆಟ್ರಾಸೈಕ್ಲಿನ್ ನೀಡಬಹುದು. ಕೆಲವು ರಾಜ್ಯಗಳಲ್ಲಿ ಲಸಿಕೆ ಲಭ್ಯ."),
            "recovery": ("Most cattle recover, but they can remain carriers and shed Coxiella in milk and birth fluids.", "अधिकांश पशु ठीक हो जाते हैं, लेकिन वाहक बने रह सकते हैं और दूध/प्रसव द्रव में बैक्टीरिया छोड़ सकते हैं।", "ಹೆಚ್ಚಿನ ಹಸುಗಳು ಗುಣಮುಖವಾಗುತ್ತವೆ, ಆದರೆ ವಾಹಕರಾಗಿ ಹಾಲು ಮತ್ತು ಜನನ ದ್ರವದಲ್ಲಿ ಕಾಕ್ಸಿಯೆಲ್ಲಾ ಬಿಡುಗಡೆ ಮಾಡಬಹುದು."),
        },
        "lsd": {
            "immediate": ("Isolate the animal to prevent insect vector spread to other cattle.", "कीट वेक्टर से अन्य पशुओं में फैलने से रोकने के लिए अलग करें।", "ಕೀಟ ವೆಕ್ಟರ್ ಇತರ ಹಸುಗಳಿಗೆ ಹರಡದಂತೆ ಪ್ರತ್ಯೇಕಿಸಿ."),
            "do_not": ("Do not move the animal off your farm. Do not allow insect exposure.", "पशु को खेत से बाहर न ले जाएँ। कीट संपर्क न होने दें।", "ಜಾನುವಾರನ್ನು ಫಾರ್ಮ್‌ನಿಂದ ಹೊರಕ್ಕೆ ತೆಗೆದುಕೊಂಡು ಹೋಗಬೇಡಿ. ಕೀಟ ಸಂಪರ್ಕಕ್ಕೆ ಅವಕಾಶ ಕೊಡಬೇಡಿ."),
            "vet_action": ("Contact a vet for supportive care (wound treatment, fly repellent). Vaccination campaign may be available in your district.", "सहायक देखभाल के लिए पशु चिकित्सक से संपर्क करें। जिले में टीकाकरण अभियान हो सकता है।", "ಬೆಂಬಲ ಆರೈಕೆಗಾಗಿ ಪಶುವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ. ನಿಮ್ಮ ಜಿಲ್ಲೆಯಲ್ಲಿ ಲಸಿಕೆ ಅಭಿಯಾನ ಇರಬಹುದು."),
            "recovery": ("Most cattle recover in 2–6 weeks with proper wound care and fly control.", "उचित घाव देखभाल और मक्खी नियंत्रण से अधिकांश 2–6 सप्ताह में ठीक हो जाते हैं।", "ಸರಿಯಾದ ಗಾಯ ಆರೈಕೆ ಮತ್ತು ನೊಣ ನಿಯಂತ್ರಣದೊಂದಿಗೆ ಹೆಚ್ಚಿನ ಹಸುಗಳು 2–6 ವಾರಗಳಲ್ಲಿ ಗುಣಮುಖವಾಗುತ್ತವೆ."),
        },
        "fmd": {
            "immediate": ("Isolate the animal. Restrict all movement on and off your farm immediately.", "पशु को अलग करें। खेत में आने-जाने पर तुरंत प्रतिबंध लगाएँ।", "ಜಾನುವಾರನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ. ಫಾರ್ಮ್‌ಗೆ ಬರುವ-ಹೋಗುವ ಎಲ್ಲಾ ಚಲನೆ ತಕ್ಷಣ ನಿರ್ಬಂಧಿಸಿ."),
            "do_not": ("Do not sell or move any cattle. FMD spreads extremely rapidly between herds.", "कोई भी पशु न बेचें या न ले जाएँ। एफएमडी झुंडों में बहुत तेज़ी से फैलता है।", "ಯಾವುದೇ ಹಸುಗಳನ್ನು ಮಾರಬೇಡಿ ಅಥವಾ ಸಾಗಿಸಬೇಡಿ. ಎಫ್ಎಂಡಿ ಕೂಪಗಳ ನಡುವೆ ಅತ್ಯಂತ ವೇಗವಾಗಿ ಹರಡುತ್ತದೆ."),
            "vet_action": ("FMD is notifiable — call your district vet officer. Vaccination of surrounding herd is the primary control measure.", "एफएमडी सूचनात्मक है — जिला पशु अधिकारी को बुलाएँ। आसपास के झुंड का टीकाकरण मुख्य उपाय है।", "ಎಫ್ಎಂಡಿ ಸೂಚನೀಯ — ಜಿಲ್ಲಾ ಪಶು ಅಧಿಕಾರಿಯನ್ನು ಕರೆ ಮಾಡಿ. ಸುತ್ತಲಿನ ಕೂಪದ ಲಸಿಕೆ ಪ್ರಮುಖ ನಿಯಂತ್ರಣ ಕ್ರಮ."),
            "recovery": ("Most cattle survive FMD but recovery can take 2–3 weeks. Milk production may drop permanently.", "अधिकांश पशु एफएमडी से बच जाते हैं लेकिन ठीक होने में 2–3 सप्ताह लग सकते हैं। दूध उत्पादन स्थायी रूप से घट सकता है।", "ಹೆಚ್ಚಿನ ಹಸುಗಳು ಎಫ್ಎಂಡಿಯಿಂದ ಬದುಕುತ್ತವೆ ಆದರೆ ಗುಣಮುಖತೆಗೆ 2–3 ವಾರ ಬೇಕಾಗಬಹುದು. ಹಾಲು ಉತ್ಪಾದನೆ ಶಾಶ್ವತವಾಗಿ ಇಳಿಯಬಹುದು."),
        },
        "ring": {
            "immediate": ("Separate the affected animal. Wear gloves when handling.", "प्रभावित पशु को अलग करें। छूते समय दस्ताने पहनें।", "ಬಾಧಿತ ಜಾನುವಾರನ್ನು ಪ್ರತ್ಯೇಕಿಸಿ. ನಿರ್ವಹಿಸುವಾಗ ಕೈಗವಸು ಧರಿಸಿ."),
            "do_not": ("Do not let children touch the animal. Do not share grooming equipment between animals.", "बच्चों को पशु न छूने दें। पशुओं के बीच संवारने का सामान साझा न करें।", "ಮಕ್ಕಳು ಜಾನುವಾರನ್ನು ಮುಟ್ಟಲು ಬಿಡಬೇಡಿ. ಜಾನುವಾರುಗಳ ನಡುವೆ ಸಂವಾರಣೆ ಉಪಕರಣ ಹಂಚಬೇಡಿ."),
            "vet_action": ("A vet can prescribe antifungal spray or iodine-based wash. Treat all contact animals.", "पशु चिकित्सक एंटीफंगल स्प्रे या आयोडीन वॉश दे सकते हैं। संपर्क वाले सभी पशुओं का इलाज करें।", "ಪಶುವೈದ್ಯರು ಆಂಟಿಫಂಗಲ್ ಸ್ಪ್ರೇ ಅಥವಾ ಐಯೋಡಿನ್ ವಾಶ್ ನೀಡಬಹುದು. ಸಂಪರ್ಕದಲ್ಲಿರುವ ಎಲ್ಲಾ ಜಾನುವಾರುಗಳಿಗೆ ಚಿಕಿತ್ಸೆ."),
            "recovery": ("Ringworm typically resolves in 1–3 months with treatment. It is not life-threatening.", "इलाज से दाद आमतौर पर 1–3 महीने में ठीक हो जाता है। यह जानलेवा नहीं।", "ಚಿಕಿತ್ಸೆಯೊಂದಿಗೆ ಬಳಪ ಸಾಮಾನ್ಯವಾಗಿ 1–3 ತಿಂಗಳಲ್ಲಿ ಗುಣವಾಗುತ್ತದೆ. ಇದು ಜೀವಕ್ಕೆ ಅಪಾಯಕಾರಿ ಅಲ್ಲ."),
        },
    }
    for disease, fields in data.items():
        for field, (en, hi, kn) in fields.items():
            g[f"guide_{disease}_{field}"] = _t(en, hi, kn)
    return g


def all_extra() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for fn in (pathway_entries, route_entries, group_entries, watch_symptom_entries, guidance_entries):
        out.update(fn())
    return out
