"""
AI Writing Assistant for ABook
Handwriting recognition → OCR → Spell check → Suggestions
Like Grammarly but for handwritten notes
"""

import re
from typing import List, Dict, Tuple, Optional

try:
    from spellchecker import SpellChecker
    SPELLCHECK_AVAILABLE = True
except ImportError:
    SPELLCHECK_AVAILABLE = False
    print("[Warning] PySpellChecker not installed. Run: pip install pyspellchecker")

try:
    import language_tool_python
    GRAMMAR_CHECK_AVAILABLE = True
except ImportError:
    GRAMMAR_CHECK_AVAILABLE = False
    print("[Warning] language-tool-python not installed. Run: pip install language-tool-python")


class WritingAssistant:
    """
    AI-powered writing assistant for handwritten text
    Features:
    - Spell checking
    - Auto-correction suggestions
    - Grammar checking
    - Word suggestions (like Grammarly)
    """
    
    def __init__(self):
        """Initialize spell checker and grammar checker"""
        # Spell checker (works offline)
        if SPELLCHECK_AVAILABLE:
            self.spell = SpellChecker()
            # Can add custom dictionary words
            self.spell.word_frequency.load_words(['ABook', 'OCR', 'JSS'])
        else:
            self.spell = None
        
        # Grammar checker (requires LanguageTool)
        if GRAMMAR_CHECK_AVAILABLE:
            try:
                self.grammar = language_tool_python.LanguageTool('en-US')
            except:
                self.grammar = None
                print("[Warning] LanguageTool server not available")
        else:
            self.grammar = None
        
        # Common corrections cache
        self.correction_cache = {}
    
    def check_spelling(self, text: str) -> List[Dict]:
        """
        Check spelling in text and return corrections
        
        Args:
            text: Input text to check
            
        Returns:
            List of {word, suggestions, position} dictionaries
        """
        if not self.spell:
            return []
        
        # Split into words
        words = re.findall(r'\b\w+\b', text)
        errors = []
        
        for word in words:
            # Check if misspelled
            if word.lower() not in self.spell and len(word) > 1:
                # Get suggestions
                suggestions = list(self.spell.candidates(word))[:5]  # Top 5
                
                # Find position in text
                position = text.lower().find(word.lower())
                
                errors.append({
                    'word': word,
                    'suggestions': suggestions,
                    'position': position,
                    'type': 'spelling'
                })
        
        return errors
    
    def check_grammar(self, text: str) -> List[Dict]:
        """
        Check grammar and return suggestions
        
        Args:
            text: Input text to check
            
        Returns:
            List of grammar issues with suggestions
        """
        if not self.grammar:
            return []
        
        try:
            matches = self.grammar.check(text)
            issues = []
            
            for match in matches:
                issues.append({
                    'message': match.message,
                    'suggestions': match.replacements[:3],  # Top 3
                    'position': match.offset,
                    'length': match.errorLength,
                    'type': 'grammar',
                    'category': match.category
                })
            
            return issues
        except:
            return []
    
    def auto_correct(self, text: str, aggressive: bool = False) -> str:
        """
        Auto-correct common spelling mistakes
        
        Args:
            text: Input text
            aggressive: If True, auto-correct all mistakes. If False, only common ones.
            
        Returns:
            Corrected text
        """
        if not self.spell:
            return text
        
        # Check cache first
        if text in self.correction_cache:
            return self.correction_cache[text]
        
        words = text.split()
        corrected_words = []
        
        for word in words:
            # Keep punctuation
            punctuation = ''
            clean_word = word
            if word and not word[-1].isalnum():
                punctuation = word[-1]
                clean_word = word[:-1]
            
            # Check if misspelled
            if clean_word.lower() not in self.spell and len(clean_word) > 1:
                # Get best correction
                correction = self.spell.correction(clean_word)
                
                if aggressive or self._is_common_mistake(clean_word, correction):
                    # Apply correction, preserve case
                    if clean_word.isupper():
                        corrected_words.append(correction.upper() + punctuation)
                    elif clean_word[0].isupper():
                        corrected_words.append(correction.capitalize() + punctuation)
                    else:
                        corrected_words.append(correction + punctuation)
                else:
                    corrected_words.append(word)
            else:
                corrected_words.append(word)
        
        result = ' '.join(corrected_words)
        self.correction_cache[text] = result
        return result
    
    def get_suggestions(self, word: str, num_suggestions: int = 5) -> List[str]:
        """
        Get spelling suggestions for a word
        
        Args:
            word: Word to get suggestions for
            num_suggestions: Number of suggestions to return
            
        Returns:
            List of suggested words
        """
        if not self.spell:
            return []
        
        candidates = self.spell.candidates(word)
        return list(candidates)[:num_suggestions] if candidates else []
    
    def add_to_dictionary(self, word: str):
        """Add a word to the custom dictionary"""
        if self.spell:
            self.spell.word_frequency.load_words([word])
    
    def _is_common_mistake(self, original: str, corrected: str) -> bool:
        """
        Determine if this is a common typo that should be auto-corrected
        
        Args:
            original: Original word
            corrected: Corrected word
            
        Returns:
            True if this is a common mistake
        """
        # Common patterns
        common_mistakes = {
            'teh': 'the',
            'adn': 'and',
            'waht': 'what',
            'thsi': 'this',
            'taht': 'that',
            'recieve': 'receive',
            'occured': 'occurred',
        }
        
        return original.lower() in common_mistakes
    
    def analyze_text(self, text: str) -> Dict:
        """
        Comprehensive text analysis
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with spelling errors, grammar issues, and statistics
        """
        analysis = {
            'spelling_errors': self.check_spelling(text),
            'grammar_issues': self.check_grammar(text),
            'word_count': len(text.split()),
            'char_count': len(text),
            'suggestions_available': SPELLCHECK_AVAILABLE or GRAMMAR_CHECK_AVAILABLE
        }
        
        return analysis


# Singleton instance
_assistant = None

def get_writing_assistant() -> WritingAssistant:
    """Get or create writing assistant instance"""
    global _assistant
    if _assistant is None:
        _assistant = WritingAssistant()
    return _assistant


if __name__ == "__main__":
    # Test the writing assistant
    assistant = WritingAssistant()
    
    # Test spelling
    test_text = "Ths is a tets of the speling checker. It shoud fnd mistkes."
    print("Original:", test_text)
    print("Corrected:", assistant.auto_correct(test_text, aggressive=True))
    print()
    
    # Test suggestions
    errors = assistant.check_spelling(test_text)
    for error in errors:
        print(f"'{error['word']}' → Suggestions: {error['suggestions']}")
    print()
    
    # Test grammar
    grammar_test = "She don't like pizza. Me and him went to store."
    grammar_issues = assistant.check_grammar(grammar_test)
    for issue in grammar_issues:
        print(f"Grammar: {issue['message']}")
        print(f"Suggestions: {issue['suggestions']}")