import re

class DynamicTokenizer:
    def __init__(self):
        self.word_to_id = {}
        self.id_to_word = {}
        self.next_id = 1

    def _clean_and_tokenize(self, text):
        """
        Cleans the text by converting it to lowercase and removing punctuation,
        then splits the text into clean word tokens.
        """
        text_lower = text.lower()
        text_clean = re.sub(r'[^\w\s]', '', text_lower)
        return text_clean.split()

    def fit_transform(self, text):
        """
        Processes text, updates the internal vocabulary with any new words found,
        and returns both the raw token list and their respective vocabulary IDs.
        """
        tokens = self._clean_and_tokenize(text)
        token_ids = []

        for token in tokens:
            if token not in self.word_to_id:
                self.word_to_id[token] = self.next_id
                self.id_to_word[self.next_id] = token
                self.next_id += 1
            
            token_ids.append(self.word_to_id[token])

        return tokens, token_ids

    def get_vocabulary(self):
        """Returns the current state of the internal vocabulary dictionary."""
        return self.word_to_id


# TESTING THE IMPLEMENTATION WITH THE ASSIGNMENT SAMPLE
if __name__ == "__main__":
    tokenizer = DynamicTokenizer()

    sample_text_1 = "This is a test. This test is simple."
    print("--- Processing Text 1 ---")
    print(f"Input: \"{sample_text_1}\"")
    
    tokens_1, ids_1 = tokenizer.fit_transform(sample_text_1)
    
    print(f"Tokens: {tokens_1}")
    print(f"Token IDs: {ids_1}")
    print(f"Vocabulary State: {tokenizer.get_vocabulary()}")
    print("-" * 50)

    sample_text_2 = "Simple text yields a new vocabulary challenge!"
    print("--- Processing Text 2 (Dynamic Expansion) ---")
    print(f"Input: \"{sample_text_2}\"")
    
    tokens_2, ids_2 = tokenizer.fit_transform(sample_text_2)
    
    print(f"Tokens: {tokens_2}")
    print(f"Token IDs: {ids_2}")
    print(f"Updated Vocabulary State: {tokenizer.get_vocabulary()}")
    print("-" * 50)