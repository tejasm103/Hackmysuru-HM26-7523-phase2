"""
AdaptiveLearn AI - AI Language Translation Engine
Translates educational transcripts, subtitles, and explanations across 6 regional languages:
- English
- Kannada (ಕನ್ನಡ)
- Hindi (हिंदी)
- Telugu (తెలుగు)
- Tamil (தமிழ்)
- Malayalam (മലയാളം)
"""

from config import Config

# High-fidelity multilingual educational terminology dictionary for demo mode
DEMO_TRANSLATIONS = {
    "kn": {
        "Statistics: Mean, Variance & Distributions": "ಅಂಕಿಅಂಶಗಳು: ಸರಾಸರಿ, ವ್ಯತ್ಯಾಸ ಮತ್ತು ಹಂಚಿಕೆಗಳು",
        "Probability: Classical, Conditional & Independent Events": "ಸಂಭವನೀಯತೆ: ಶಾಸ್ತ್ರೀಯ, ಷರತ್ತುಬದ್ಧ ಮತ್ತು ಸ್ವತಂತ್ರ ಘಟನೆಗಳು",
        "Why Do We Square Differences in Variance?": "ವ್ಯತ್ಯಾಸದಲ್ಲಿ ನಾವು ವ್ಯತ್ಯಾಸಗಳನ್ನು ಏಕೆ ವರ್ಗಗೊಳಿಸುತ್ತೇವೆ?",
        "Save the Space Station: Orbital Resource Equilibrium": "ಬಾಹ್ಯಾಕಾಶ ನಿಲ್ದಾಣವನ್ನು ರಕ್ಷಿಸಿ: ಕಕ್ಷೆಯ ಸಂಪನ್ಮೂಲ ಸಮತೋಲನ",
        "Mastered": "ಪಾರಂಗತ (ಮಾಸ್ಟರ್ಡ್)",
        "Learning": "ಕಲಿಯುತ್ತಿದ್ದಾರೆ",
        "Needs Practice": "ಅಭ್ಯಾಸದ ಅಗತ್ಯವಿದೆ",
        "Struggling": "ಸಹಾಯ ಬೇಕಾಗಿದೆ",
        "Locked": "ಲಾಕ್ ಆಗಿದೆ",
        "sample_transcript": "ವಿದ್ಯಾರ್ಥಿಗಳೇ ಸ್ವಾಗತ. ಇಂದು ನಾವು ವಿಚಲನದ ಅಳತೆಗಳು, ಸರಾಸರಿ ವಿಚಲನೆಗಳು ಮತ್ತು ಡೇಟಾಸೆಟ್‌ಗಳಲ್ಲಿನ ವ್ಯತ್ಯಾಸವನ್ನು ಹೇಗೆ ಅಳೆಯುವುದು ಎಂಬುದನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತೇವೆ."
    },
    "hi": {
        "Statistics: Mean, Variance & Distributions": "सांख्यिकी: माध्य, प्रसरण और वितरण",
        "Probability: Classical, Conditional & Independent Events": "प्रायिकता: शास्त्रीय, सशर्त और स्वतंत्र घटनाएं",
        "Why Do We Square Differences in Variance?": "प्रसरण में हम अंतरों का वर्ग क्यों करते हैं?",
        "Save the Space Station: Orbital Resource Equilibrium": "अंतरिक्ष स्टेशन को बचाएं: कक्षीय संसाधन संतुलन",
        "Mastered": "महारत हासिल",
        "Learning": "सीख रहे हैं",
        "Needs Practice": "अभ्यास की आवश्यकता",
        "Struggling": "सहायता की आवश्यकता",
        "Locked": "लॉक किया गया",
        "sample_transcript": "विद्यार्थियों का स्वागत है। आज हम विचलन के माप, माध्य विचलन और डेटासेट में परिवर्तनशीलता को मापने के तरीकों का विश्लेषण करेंगे।"
    },
    "te": {
        "Statistics: Mean, Variance & Distributions": "గణాంకాలు: సగటు, వైవిధ్యం మరియు పంపిణీలు",
        "Probability: Classical, Conditional & Independent Events": "సంభావ్యత: సాంప్రదాయ, షరతులతో కూడిన మరియు స్వతంత్ర సంఘటనలు",
        "Why Do We Square Differences in Variance?": "వైవిధ్యంలో తేడాలను మనం ఎందుకు వర్గం చేస్తాం?",
        "Save the Space Station: Orbital Resource Equilibrium": "స్పేస్ స్టేషన్‌ను రక్షించండి: కక్ష్య వనరుల సమతుల్యత",
        "Mastered": "ప్రావీణ్యం",
        "Learning": "నేర్చుకుంటున్నారు",
        "Needs Practice": "అభ్యాసం అవసరం",
        "Struggling": "సహాయం కావాలి",
        "Locked": "లాక్ చేయబడింది",
        "sample_transcript": "విద్యార్థులకు స్వాగతం. ఈరోజు మనం విస్తరణ కొలతలు, సగటు విచలనాలు మరియు డేటాసెట్‌లలో వైవిధ్యాన్ని ఎలా లెక్కించాలో విశ్లేషిస్తాము."
    },
    "ta": {
        "Statistics: Mean, Variance & Distributions": "புள்ளியியல்: சராசரி, மாறுபாடு மற்றும் பரவல்கள்",
        "Probability: Classical, Conditional & Independent Events": "நிகழ்தகவு: மரபுவழி, நிபந்தனை மற்றும் சார்பற்ற நிகழ்வுகள்",
        "Why Do We Square Differences in Variance?": "மாறுபாட்டில் நாம் ஏன் வித்தியாசங்களை வர்க்கப்படுத்துகிறோம்?",
        "Save the Space Station: Orbital Resource Equilibrium": "விண்வெளி நிலையத்தை காப்பாற்றுங்கள்: சுற்றுப்பாதை வள சமநிலை",
        "Mastered": "தேர்ச்சி பெற்றது",
        "Learning": "கற்றுக்கொள்கிறார்",
        "Needs Practice": "பயிற்சி தேவை",
        "Struggling": "உதவி தேவை",
        "Locked": "பூட்டப்பட்டது",
        "sample_transcript": "மாணவர்களுக்கு வணக்கம். இன்று நாம் விலகல் அளவீடுகள், சராசரி விலகல்கள் மற்றும் தரவுத்தொகுப்புகளின் மாறுபாட்டை அளவிடுவது பற்றி ஆய்வு செய்வோம்."
    },
    "ml": {
        "Statistics: Mean, Variance & Distributions": "സ്ഥിതിവിവരക്കണക്കുകൾ: ശരാശരി, വ്യതിയാനം, വിതരണങ്ങൾ",
        "Probability: Classical, Conditional & Independent Events": "സംഭാവ്യത: ക്ലാസിക്കൽ, സോപാധിക, സ്വതന്ത്ര ഇവന്റുകൾ",
        "Why Do We Square Differences in Variance?": "വ്യതിയാനത്തിൽ വ്യത്യാസങ്ങൾ ഞങ്ങൾ സ്ക്വയർ ചെയ്യുന്നത് എന്തുകൊണ്ട്?",
        "Save the Space Station: Orbital Resource Equilibrium": "ബഹിരാകാശ നിലയം സംരക്ഷിക്കുക: ഭ്രമണപഥ വിഭവ സന്തുലിതാവസ്ഥ",
        "Mastered": "പ്രാവീണ്യം നേടി",
        "Learning": "പഠിക്കുന്നു",
        "Needs Practice": "പരിശീലനം ആവശ്യമാണ്",
        "Struggling": "സഹായം ആവശ്യമാണ്",
        "Locked": "പൂട്ടിയിരിക്കുന്നു",
        "sample_transcript": "വിദ്യാർത്ഥികൾക്ക് സ്വാഗതം. ഇന്ന് നമ്മൾ ഡാറ്റാസെറ്റുകളിലെ വ്യതിയാനങ്ങൾ എങ്ങിനെ അളക്കാമെന്ന് വിശകലനം ചെയ്യുന്നു."
    }
}

def translate_content(text, target_language="en", context_type="general"):
    """
    Translates educational text into target language.
    Falls back gracefully to high-accuracy domain dictionaries in demo mode.
    """
    if not text or target_language.lower() in ("en", "english"):
        return text

    target_code = target_language.lower()[:2]
    
    # Try Live Gemini Translation if API key is present
    if Config.GEMINI_API_KEY:
        try:
            import google.genai as genai
            client = genai.Client(api_key=Config.GEMINI_API_KEY)
            prompt = f"Translate the following educational text into {target_language} accurately. Preserve mathematical notations and numbers:\n\n{text}"
            res = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            if res.text:
                return res.text.strip()
        except Exception as e:
            print(f"[AI Translation] API notice: {e}")

    # High-Fidelity Demo Translation Fallback
    lang_dict = DEMO_TRANSLATIONS.get(target_code, {})
    if text in lang_dict:
        return lang_dict[text]
        
    for k, v in lang_dict.items():
        if k.lower() in text.lower():
            return v
            
    # Generic prefix fallback for non-dictionary phrases in demo mode
    prefixes = {
        "kn": "[ಕನ್ನಡ ಅನುವಾದ] ",
        "hi": "[हिंदी अनुवाद] ",
        "te": "[తెలుగు అనువాదం] ",
        "ta": "[தமிழ் மொழிபெயர்ப்பு] ",
        "ml": "[മലയാളം വിവർത്തനം] "
    }
    return f"{prefixes.get(target_code, '')}{text}"
