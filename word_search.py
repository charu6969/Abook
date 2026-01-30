"""
Dictionary and word search functionality
"""
import requests
import json


class WordSearcher:
    """Search for word meanings and suggestions"""
    
    def __init__(self):
        self.cache = {}  # Cache results
    
    def search_definition(self, word):
        """
        Search for word definition using Free Dictionary API
        Returns: dict with definition, synonyms, etc.
        """
        word = word.lower().strip()
        
        # Check cache first
        if word in self.cache:
            return self.cache[word]
        
        try:
            # Use Free Dictionary API
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                result = self._parse_dictionary_response(data)
                self.cache[word] = result
                return result
            else:
                return {
                    'word': word,
                    'found': False,
                    'error': 'Word not found in dictionary'
                }
        
        except requests.RequestException as e:
            return {
                'word': word,
                'found': False,
                'error': 'Could not connect to dictionary service'
            }
        except Exception as e:
            return {
                'word': word,
                'found': False,
                'error': str(e)
            }
    
    def _parse_dictionary_response(self, data):
        """Parse the API response"""
        if not data or len(data) == 0:
            return {'found': False}
        
        entry = data[0]
        word = entry.get('word', '')
        
        # Extract definitions
        definitions = []
        synonyms = []
        antonyms = []
        
        for meaning in entry.get('meanings', []):
            part_of_speech = meaning.get('partOfSpeech', '')
            
            for definition in meaning.get('definitions', []):
                definitions.append({
                    'pos': part_of_speech,
                    'definition': definition.get('definition', ''),
                    'example': definition.get('example', '')
                })
                
                # Collect synonyms and antonyms
                synonyms.extend(definition.get('synonyms', []))
                antonyms.extend(definition.get('antonyms', []))
        
        # Get phonetic
        phonetic = entry.get('phonetic', '')
        if not phonetic and entry.get('phonetics'):
            for p in entry.get('phonetics', []):
                if p.get('text'):
                    phonetic = p.get('text')
                    break
        
        return {
            'word': word,
            'found': True,
            'phonetic': phonetic,
            'definitions': definitions[:3],  # Limit to 3 definitions
            'synonyms': list(set(synonyms))[:5],  # Limit to 5 unique synonyms
            'antonyms': list(set(antonyms))[:5]
        }
    
    def get_suggestions(self, partial_word):
        """
        Get word suggestions (simple implementation)
        In a full app, this would use a proper word suggestion API
        """
        # This is a simple placeholder
        # In production, you'd use a proper spell-check/autocomplete API
        common_words = [
            'hello', 'world', 'python', 'programming', 'computer',
            'notebook', 'drawing', 'writing', 'learning', 'education',
            'science', 'mathematics', 'history', 'geography', 'literature'
        ]
        
        partial = partial_word.lower()
        suggestions = [w for w in common_words if w.startswith(partial)]
        return suggestions[:5]


class OfflineDictionary:
    """
    Simple offline dictionary fallback
    Contains basic definitions for common words
    """
    
    def __init__(self):
        self.definitions = {
            'hello': 'A greeting or expression of goodwill',
            'world': 'The earth and all its inhabitants',
            'note': 'A brief record of something written down',
            'book': 'A written or printed work consisting of pages',
            'write': 'To mark letters, words, or symbols on a surface',
            'draw': 'To produce a picture or diagram',
            'learn': 'To gain knowledge or skill by studying',
            'read': 'To look at and understand written words',
            'think': 'To have a particular opinion or idea',
            'create': 'To bring something into existence'
        }
    
    def search(self, word):
        """Search offline dictionary"""
        word = word.lower().strip()
        
        if word in self.definitions:
            return {
                'word': word,
                'found': True,
                'definition': self.definitions[word],
                'source': 'offline'
            }
        else:
            return {
                'word': word,
                'found': False,
                'error': 'Word not in offline dictionary'
            }