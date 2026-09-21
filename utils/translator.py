"""
Multilingual Translation Module
Supports: English, Hindi, Tamil, Telugu, Kannada, Bengali
Uses Google Translate API for dynamic translations
"""

import os
import json
from typing import Dict, Optional
from functools import lru_cache

try:
    from googletrans import Translator
    TRANSLATOR_AVAILABLE = True
except Exception as e:
    TRANSLATOR_AVAILABLE = False
    print(f"[WARNING] Translation service unavailable: {e}")
    Translator = None

# Supported languages
LANGUAGES = {
    'en': {'name': 'English', 'flag': '🇬🇧', 'native': 'English'},
    'hi': {'name': 'Hindi', 'flag': '🇮🇳', 'native': 'हिन्दी'},
    'ta': {'name': 'Tamil', 'flag': '🇮🇳', 'native': 'தமிழ்'},
    'te': {'name': 'Telugu', 'flag': '🇮🇳', 'native': 'తెలుగు'},
    'kn': {'name': 'Kannada', 'flag': '🇮🇳', 'native': 'ಕನ್ನಡ'},
    'bn': {'name': 'Bengali', 'flag': '🇮🇳', 'native': 'বাংলা'}
}

# Nutrition and app-specific translations (pre-translated for accuracy)
TRANSLATIONS = {
    'en': {
        'app_title': 'AI Nutrition Advisor',
        'meal_planner': 'Meal Planner',
        'usda_lookup': 'USDA Food Lookup',
        'health_info': 'Health Information',
        'immunisation': 'Immunisation',
        'growth_tracking': 'Growth Tracking',
        'who_vaccines': 'WHO Vaccines',
        'ai_chatbot': 'AI Chatbot',
        'analytics': 'Analytics',
        'about': 'About',
        
        # Common phrases
        'welcome': 'Welcome',
        'save': 'Save',
        'cancel': 'Cancel',
        'submit': 'Submit',
        'delete': 'Delete',
        'edit': 'Edit',
        'search': 'Search',
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        
        # Nutrition terms
        'protein': 'Protein',
        'carbohydrates': 'Carbohydrates',
        'fat': 'Fat',
        'calories': 'Calories',
        'vitamins': 'Vitamins',
        'minerals': 'Minerals',
        'iron': 'Iron',
        'calcium': 'Calcium',
        'fiber': 'Fiber',
        
        # Meal planning
        'breakfast': 'Breakfast',
        'lunch': 'Lunch',
        'snack': 'Snack',
        'dinner': 'Dinner',
        'meal_plan': 'Meal Plan',
        'ingredients': 'Ingredients',
        'recipe': 'Recipe',
        
        # Health
        'age': 'Age',
        'weight': 'Weight',
        'height': 'Height',
        'bmi': 'BMI',
        'allergies': 'Allergies',
        'dietary_preferences': 'Dietary Preferences',
        'vegetarian': 'Vegetarian',
        'vegan': 'Vegan',
        'non_veg': 'Non-Vegetarian',
        
    # UI labels
    'number_of_children': 'Number of Children',
    'weekly_budget': 'Weekly Budget (₹)',
    'age_group_label': 'Age Group',
    'exclude_allergens': 'Exclude Allergens',
    'select_all': 'Select All',
    'clear_all': 'Clear All',
    'recommended': 'Recommended',
    'ingredients_selected': '{count} ingredients selected',
    'generate_meal_plan': 'Generate Meal Plan',
    'optimizing_meal_plan': 'Optimizing meal plan...',
    'this_may_take': 'This may take 10-20 seconds',
    'download_csv': 'Download CSV',
    'download_pdf': 'Download PDF',
    'download_json': 'Download JSON',
    'print': 'Print',
    'scan_to_share_plan': 'Scan to share plan',

        # Metrics
        'total_cost': 'Total Cost',
        'nutrition_score': 'Nutrition Score',
        'avg_daily_calories': 'Avg Daily Calories',
        'avg_daily_protein': 'Avg Daily Protein',

        # Messages
        'meal_plan_saved': 'Meal plan saved successfully!',
    'clear_chat': 'Clear Chat',
        'data_updated': 'Data updated successfully!',
        'error_occurred': 'An error occurred. Please try again.',
    },
    'hi': {
        'app_title': 'एआई पोषण सलाहकार',
        'meal_planner': 'भोजन योजनाकार',
        'usda_lookup': 'USDA खाद्य खोज',
        'health_info': 'स्वास्थ्य जानकारी',
        'immunisation': 'टीकाकरण',
        'growth_tracking': 'विकास ट्रैकिंग',
        'who_vaccines': 'WHO टीके',
        'ai_chatbot': 'एआई चैटबॉट',
        'analytics': 'विश्लेषण',
        'about': 'के बारे में',
        
        'welcome': 'स्वागत है',
        'save': 'सहेजें',
        'cancel': 'रद्द करें',
        'submit': 'जमा करें',
        'delete': 'हटाएं',
        'edit': 'संपादित करें',
        'search': 'खोजें',
        'loading': 'लोड हो रहा है...',
        'error': 'त्रुटि',
        'success': 'सफलता',
        
        'protein': 'प्रोटीन',
        'carbohydrates': 'कार्बोहाइड्रेट',
        'fat': 'वसा',
        'calories': 'कैलोरी',
        'vitamins': 'विटामिन',
        'minerals': 'खनिज',
        'iron': 'लोहा',
        'calcium': 'कैल्शियम',
        'fiber': 'फाइबर',
        
        'breakfast': 'नाश्ता',
        'lunch': 'दोपहर का भोजन',
        'snack': 'नाश्ता',
        'dinner': 'रात का खाना',
        'meal_plan': 'भोजन योजना',
        'ingredients': 'सामग्री',
        'recipe': 'विधि',
        
        'age': 'उम्र',
        'weight': 'वजन',
        'height': 'ऊंचाई',
        'bmi': 'बीएमआई',
        'allergies': 'एलर्जी',
        'dietary_preferences': 'आहार वरीयताएँ',
        'vegetarian': 'शाकाहारी',
        'vegan': 'शुद्ध शाकाहारी',
    'non_veg': 'मांसाहारी',
    # UI labels
    'number_of_children': 'बच्चों की संख्या',
    'weekly_budget': 'साप्ताहिक बजट (₹)',
    'age_group_label': 'आयु समूह',
    'exclude_allergens': 'एलर्जी हटाएं',
    'select_all': 'सभी चुनें',
    'clear_all': 'सभी हटाएं',
    'recommended': 'अनुशंसित',
    'ingredients_selected': '{count} सामग्री चुनी गईं',
    'generate_meal_plan': 'भोजन योजना बनाएं',
    'optimizing_meal_plan': 'भोजन योजना अनुकूलित की जा रही है...',
    'this_may_take': 'यह 10-20 सेकंड ले सकता है',
    'download_csv': 'CSV डाउनलोड करें',
    'download_pdf': 'PDF डाउनलोड करें',
    'download_json': 'JSON डाउनलोड करें',
    'print': 'प्रिंट करें',
    'scan_to_share_plan': 'योजना साझा करने के लिए स्कैन करें',

        # Metrics
        'total_cost': 'कुल लागत',
        'nutrition_score': 'पोषण स्कोर',
        'avg_daily_calories': 'औसत दैनिक कैलोरी',
        'avg_daily_protein': 'औसत दैनिक प्रोटीन',

        
    'meal_plan_saved': 'भोजन योजना सफलतापूर्वक सहेजी गई!',
    'clear_chat': 'चैट साफ़ करें',
        'data_updated': 'डेटा सफलतापूर्वक अपडेट किया गया!',
        'error_occurred': 'एक त्रुटि उत्पन्न हुई। कृपया पुनः प्रयास करें।',
    },
    'ta': {
        'app_title': 'AI ஊட்டச்சத்து ஆலோசகர்',
        'meal_planner': 'உணவு திட்டமிடுபவர்',
        'usda_lookup': 'USDA உணவு தேடல்',
        'health_info': 'சுகாதார தகவல்',
        'immunisation': 'தடுப்பூசி',
        'growth_tracking': 'வளர்ச்சி கண்காணிப்பு',
        'who_vaccines': 'WHO தடுப்பூசிகள்',
        'ai_chatbot': 'AI அரட்டை',
        'analytics': 'பகுப்பாய்வு',
        'about': 'பற்றி',
        
        'welcome': 'வரவேற்கிறோம்',
        'save': 'சேமி',
        'cancel': 'ரத்து செய்',
        'submit': 'சமர்ப்பி',
        'delete': 'நீக்கு',
        'edit': 'தொகு',
        'search': 'தேடு',
        'loading': 'ஏற்றுகிறது...',
        'error': 'பிழை',
        'success': 'வெற்றி',
        
        'protein': 'புரதம்',
        'carbohydrates': 'கார்போஹைட்ரேட்',
        'fat': 'கொழுப்பு',
        'calories': 'கலோரி',
        'vitamins': 'வைட்டமின்கள்',
        'minerals': 'தாதுக்கள்',
        'iron': 'இரும்பு',
        'calcium': 'கால்சியம்',
        'fiber': 'நார்ச்சத்து',
        
        'breakfast': 'காலை உணவு',
        'lunch': 'மதிய உணவு',
        'snack': 'சிற்றுண்டி',
        'dinner': 'இரவு உணவு',
        'meal_plan': 'உணவு திட்டம்',
        'ingredients': 'பொருட்கள்',
        'recipe': 'செய்முறை',
        
        'age': 'வயது',
        'weight': 'எடை',
        'height': 'உயரம்',
        'bmi': 'பிஎம்ஐ',
        'allergies': 'ஒவ்வாமை',
        'dietary_preferences': 'உணவு விருப்பங்கள்',
        'vegetarian': 'சைவ உணவு',
        'vegan': 'தூய சைவம்',
        'non_veg': 'அசைவ உணவு',
        
        'meal_plan_saved': 'உணவு திட்டம் வெற்றிகரமாக சேமிக்கப்பட்டது!',
        'data_updated': 'தரவு வெற்றிகரமாக புதுப்பிக்கப்பட்டது!',
        'error_occurred': 'ஒரு பிழை ஏற்பட்டது. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.',
    },
    'te': {
        'app_title': 'AI పోషణ సలహాదారు',
        'meal_planner': 'భోజన ప్రణాళిక',
        'usda_lookup': 'USDA ఆహార శోధన',
        'health_info': 'ఆరోగ్య సమాచారం',
        'immunisation': 'టీకాలు',
        'growth_tracking': 'వృద్ధి ట్రాకింగ్',
        'who_vaccines': 'WHO టీకాలు',
        'ai_chatbot': 'AI చాట్‌బాట్',
        'analytics': 'విశ్లేషణ',
        'about': 'గురించి',
        
        'welcome': 'స్వాగతం',
        'save': 'సేవ్ చేయండి',
        'cancel': 'రద్దు చేయండి',
        'submit': 'సమర్పించండి',
        'delete': 'తొలగించండి',
        'edit': 'సవరించండి',
        'search': 'వెతకండి',
        'loading': 'లోడ్ అవుతోంది...',
        'error': 'లోపం',
        'success': 'విజయం',
        
        'protein': 'ప్రోటీన్',
        'carbohydrates': 'కార్బోహైడ్రేట్లు',
        'fat': 'కొవ్వు',
        'calories': 'కేలరీలు',
        'vitamins': 'విటమిన్లు',
        'minerals': 'ఖనిజాలు',
        'iron': 'ఇనుము',
        'calcium': 'కాల్షియం',
        'fiber': 'ఫైబర్',
        
        'breakfast': 'అల్పాహారం',
        'lunch': 'మధ్యాహ్న భోజనం',
        'snack': 'స్నాక్',
        'dinner': 'రాత్రి భోజనం',
        'meal_plan': 'భోజన ప్రణాళిక',
        'ingredients': 'పదార్థాలు',
        'recipe': 'వంట విధానం',
        
        'age': 'వయస్సు',
        'weight': 'బరువు',
        'height': 'ఎత్తు',
        'bmi': 'BMI',
        'allergies': 'అలెర్జీలు',
        'dietary_preferences': 'ఆహార ప్రాధాన్యతలు',
        'vegetarian': 'శాకాహారం',
        'vegan': 'శుద్ధ శాకాహారం',
        'non_veg': 'మాంసాహారం',
        
        'meal_plan_saved': 'భోజన ప్రణాళిక విజయవంతంగా సేవ్ చేయబడింది!',
        'data_updated': 'డేటా విజయవంతంగా నవీకరించబడింది!',
        'error_occurred': 'లోపం సంభవించింది. దయచేసి మళ్లీ ప్రయత్నించండి.',
    },
    'kn': {
        'app_title': 'AI ಪೋಷಣೆ ಸಲಹೆಗಾರ',
        'meal_planner': 'ಊಟದ ಯೋಜಕ',
        'usda_lookup': 'USDA ಆಹಾರ ಹುಡುಕಾಟ',
        'health_info': 'ಆರೋಗ್ಯ ಮಾಹಿತಿ',
        'immunisation': 'ಲಸಿಕೆ',
        'growth_tracking': 'ಬೆಳವಣಿಗೆ ಟ್ರ್ಯಾಕಿಂಗ್',
        'who_vaccines': 'WHO ಲಸಿಕೆಗಳು',
        'ai_chatbot': 'AI ಚಾಟ್‌ಬಾಟ್',
        'analytics': 'ವಿಶ್ಲೇಷಣೆ',
        'about': 'ಬಗ್ಗೆ',
        
        'welcome': 'ಸ್ವಾಗತ',
        'save': 'ಉಳಿಸಿ',
        'cancel': 'ರದ್ದುಮಾಡಿ',
        'submit': 'ಸಲ್ಲಿಸಿ',
        'delete': 'ಅಳಿಸಿ',
        'edit': 'ಸಂಪಾದಿಸಿ',
        'search': 'ಹುಡುಕಿ',
        'loading': 'ಲೋಡ್ ಆಗುತ್ತಿದೆ...',
        'error': 'ದೋಷ',
        'success': 'ಯಶಸ್ಸು',
        
        'protein': 'ಪ್ರೋಟೀನ್',
        'carbohydrates': 'ಕಾರ್ಬೋಹೈಡ್ರೇಟ್‌ಗಳು',
        'fat': 'ಕೊಬ್ಬು',
        'calories': 'ಕ್ಯಾಲೊರಿಗಳು',
        'vitamins': 'ವಿಟಮಿನ್‌ಗಳು',
        'minerals': 'ಖನಿಜಗಳು',
        'iron': 'ಕಬ್ಬಿಣ',
        'calcium': 'ಕ್ಯಾಲ್ಸಿಯಂ',
        'fiber': 'ಫೈಬರ್',
        
        'breakfast': 'ಬೆಳಗಿನ ಉಪಾಹಾರ',
        'lunch': 'ಮಧ್ಯಾಹ್ನದ ಊಟ',
        'snack': 'ತಿಂಡಿ',
        'dinner': 'ರಾತ್ರಿಯ ಊಟ',
        'meal_plan': 'ಊಟದ ಯೋಜನೆ',
        'ingredients': 'ಪದಾರ್ಥಗಳು',
        'recipe': 'ಪಾಕವಿಧಾನ',
        
        'age': 'ವಯಸ್ಸು',
        'weight': 'ತೂಕ',
        'height': 'ಎತ್ತರ',
        'bmi': 'BMI',
        'allergies': 'ಅಲರ್ಜಿಗಳು',
        'dietary_preferences': 'ಆಹಾರ ಆದ್ಯತೆಗಳು',
        'vegetarian': 'ಸಸ್ಯಾಹಾರಿ',
        'vegan': 'ಶುದ್ಧ ಸಸ್ಯಾಹಾರಿ',
        'non_veg': 'ಮಾಂಸಾಹಾರಿ',
        
        'meal_plan_saved': 'ಊಟದ ಯೋಜನೆಯನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ!',
        'data_updated': 'ಡೇಟಾವನ್ನು ಯಶಸ್ವಿಯಾಗಿ ನವೀಕರಿಸಲಾಗಿದೆ!',
        'error_occurred': 'ದೋಷ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.',
    },
    'bn': {
        'app_title': 'AI পুষ্টি পরামর্শদাতা',
        'meal_planner': 'খাবার পরিকল্পনাকারী',
        'usda_lookup': 'USDA খাদ্য অনুসন্ধান',
        'health_info': 'স্বাস্থ্য তথ্য',
        'immunisation': 'টিকাকরণ',
        'growth_tracking': 'বৃদ্ধি ট্র্যাকিং',
        'who_vaccines': 'WHO টিকা',
        'ai_chatbot': 'AI চ্যাটবট',
        'analytics': 'বিশ্লেষণ',
        'about': 'সম্পর্কে',
        
        'welcome': 'স্বাগতম',
        'save': 'সংরক্ষণ করুন',
        'cancel': 'বাতিল করুন',
        'submit': 'জমা দিন',
        'delete': 'মুছুন',
        'edit': 'সম্পাদনা করুন',
        'search': 'অনুসন্ধান করুন',
        'loading': 'লোড হচ্ছে...',
        'error': 'ত্রুটি',
        'success': 'সফলতা',
        
        'protein': 'প্রোটিন',
        'carbohydrates': 'কার্বোহাইড্রেট',
        'fat': 'চর্বি',
        'calories': 'ক্যালোরি',
        'vitamins': 'ভিটামিন',
        'minerals': 'খনিজ',
        'iron': 'লোহা',
        'calcium': 'ক্যালসিয়াম',
        'fiber': 'ফাইবার',
        
        'breakfast': 'সকালের নাস্তা',
        'lunch': 'দুপুরের খাবার',
        'snack': 'জলখাবার',
        'dinner': 'রাতের খাবার',
        'meal_plan': 'খাবার পরিকল্পনা',
        'ingredients': 'উপাদান',
        'recipe': 'রেসিপি',
        
        'age': 'বয়স',
        'weight': 'ওজন',
        'height': 'উচ্চতা',
        'bmi': 'BMI',
        'allergies': 'অ্যালার্জি',
        'dietary_preferences': 'খাদ্য পছন্দ',
        'vegetarian': 'নিরামিষ',
        'vegan': 'বিশুদ্ধ নিরামিষ',
        'non_veg': 'মাংসাহারী',
        
        'meal_plan_saved': 'খাবার পরিকল্পনা সফলভাবে সংরক্ষিত হয়েছে!',
        'data_updated': 'ডেটা সফলভাবে আপডেট করা হয়েছে!',
        'error_occurred': 'একটি ত্রুটি ঘটেছে। অনুগ্রহ করে আবার চেষ্টা করুন।',
    }
}


class TranslationService:
    """Translation service for the nutrition advisor app"""
    
    def __init__(self):
        """Initialize the translation service"""
        self.translator = None
        if TRANSLATOR_AVAILABLE and Translator is not None:
            try:
                self.translator = Translator()
            except Exception as e:
                print(f"⚠️ Translation service initialization failed: {e}")
                self.translator = None
    
    @lru_cache(maxsize=1000)
    def translate(self, text: str, target_lang: str, source_lang: str = 'en') -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Source language code (default: 'en')
            
        Returns:
            Translated text or original text if translation fails
        """
        # Return original if target is English
        if target_lang == 'en':
            return text
        
        # Check if we have a pre-translated version
        if target_lang in TRANSLATIONS:
            # Try to find exact match in translations
            for key, value in TRANSLATIONS[source_lang].items():
                if value.lower() == text.lower():
                    return TRANSLATIONS[target_lang].get(key, text)
        
        # Use Google Translate for dynamic content
        if self.translator and TRANSLATOR_AVAILABLE:
            try:
                result = self.translator.translate(text, dest=target_lang, src=source_lang)
                return result.text
            except Exception as e:
                print(f"Translation error: {e}")
                return text
        
        return text
    
    def get_translation(self, key: str, lang: str = 'en') -> str:
        """
        Get pre-translated text by key
        
        Args:
            key: Translation key
            lang: Language code
            
        Returns:
            Translated text or key if not found
        """
        if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
            return TRANSLATIONS[lang][key]
        return key
    
    def get_languages(self) -> Dict[str, Dict[str, str]]:
        """Get list of supported languages"""
        return LANGUAGES
    
    def is_available(self) -> bool:
        """Check if translation service is available"""
        return TRANSLATOR_AVAILABLE and self.translator is not None


# Global translation service instance
_translation_service = None

def get_translation_service() -> TranslationService:
    """Get or create the global translation service instance"""
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service


# Template helper function
def t(key: str, lang: str = 'en') -> str:
    """
    Quick translation helper for templates
    
    Args:
        key: Translation key
        lang: Language code
        
    Returns:
        Translated text
    """
    service = get_translation_service()
    return service.get_translation(key, lang)
