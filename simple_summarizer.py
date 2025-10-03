"""
Simple Text Summarizer (Frequency-Based)

This script provides a lightweight, dependency-free text summarization tool
that can be run from the command line. It works by scoring sentences based
on the frequency of their constituent non-stop words, then selecting the
highest-scoring sentences for the summary.

Usage:
    python simple_summarizer.py <filepath> [summary_ratio]

    <filepath>: Path to the text file to summarize.
    [summary_ratio]: Optional float (0.0 to 1.0) indicating the desired
                     length of the summary relative to the original text.
                     (e.g., 0.2 means 20% of the original sentences).
                     Defaults to 0.2 (20%).
"""

import sys
import re
from collections import defaultdict
from heapq import nlargest

# A simple list of common English stop words. For a robust solution,
# this list could be expanded significantly or loaded from an external source.
STOP_WORDS = set([
    'a', 'an', 'and', 'the', 'is', 'are', 'was', 'were', 'he', 'she', 'it',
    'i', 'you', 'we', 'they', 'him', 'her', 'us', 'them', 'my', 'your',
    'our', 'their', 'this', 'that', 'these', 'those', 'of', 'in', 'on',
    'at', 'to', 'for', 'with', 'as', 'by', 'but', 'so', 'if', 'or', 'up',
    'down', 'out', 'into', 'from', 'about', 'just', 'can', 'will', 'would',
    'should', 'has', 'have', 'had', 'do', 'does', 'did', 'be', 'being', 'been'
])

def preprocess_text(text):
    """
    Cleans and tokenizes the text into sentences and words.

    Args:
        text (str): The input text content.

    Returns:
        tuple: A tuple containing (list of sentences, list of words).
    """
    # 1. Tokenize into sentences
    # Finds strings ending with '.', '!', or '?', optionally followed by whitespace.
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    # 2. Tokenize into words, remove punctuation, and convert to lower case
    words = re.findall(r'\b\w+\b', text.lower())

    return sentences, words

def calculate_word_frequencies(words):
    """
    Calculates the frequency of each non-stop word in the text.

    Args:
        words (list): List of all words in the text.

    Returns:
        dict: A dictionary mapping non-stop words to their frequency count.
    """
    word_frequencies = defaultdict(int)

    for word in words:
        if word not in STOP_WORDS:
            word_frequencies[word] += 1

    return word_frequencies

def score_sentences(sentences, word_frequencies):
    """
    Scores each sentence based on the total frequency of its constituent words.

    Args:
        sentences (list): List of sentence strings.
        word_frequencies (dict): Dictionary of word frequencies.

    Returns:
        dict: A dictionary mapping sentence index to its score.
    """
    sentence_scores = defaultdict(int)

    for i, sentence in enumerate(sentences):
        # Find all words in the sentence
        sentence_words = re.findall(r'\b\w+\b', sentence.lower())

        for word in sentence_words:
            if word in word_frequencies:
                # Add the word's overall frequency to the sentence's score
                sentence_scores[i] += word_frequencies[word]

    return sentence_scores

def summarize_text(text, ratio=0.2):
    """
    Generates a summary of the input text using the frequency-based method.

    Args:
        text (str): The input text content.
        ratio (float): The desired length of the summary as a ratio of
                       original sentences (0.0 to 1.0).

    Returns:
        str: The generated summary text.
    """
    if not text:
        return "Error: Input text is empty."

    # Step 1: Preprocess and tokenize
    sentences, words = preprocess_text(text)

    # Step 2: Calculate word importance
    word_frequencies = calculate_word_frequencies(words)

    # Handle case where no meaningful words are found
    if not word_frequencies:
        return "Error: Could not calculate word frequencies (text may contain only stop words or be too short)."

    # Step 3: Score sentences
    sentence_scores = score_sentences(sentences, word_frequencies)

    # Step 4: Determine summary length
    num_sentences = len(sentences)
    summary_sentences_count = max(1, int(num_sentences * ratio))

    # Step 5: Select the top-scoring sentences
    # Get the indices (keys) of the top 'summary_sentences_count' scores
    # nlargest returns a list of tuples (score, index). We only need the indices.
    top_sentence_indices_with_scores = nlargest(
        summary_sentences_count,
        sentence_scores.items(),
        key=lambda item: item[1]
    )

    # Extract just the original index (the key in the dictionary)
    # The summary must maintain the original order of sentences, so we sort the indices.
    top_indices = sorted([index for index, score in top_sentence_indices_with_scores])

    # Step 6: Build the final summary
    summary_parts = [sentences[i] for i in top_indices]
    summary = ' '.join(summary_parts)

    return summary

def main():
    """Handles command-line interface logic."""
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python simple_summarizer.py <filepath> [summary_ratio]")
        sys.exit(1)

    filepath = sys.argv[1]
    ratio = 0.2  # Default ratio

    if len(sys.argv) == 3:
        try:
            ratio = float(sys.argv[2])
            if not 0.0 < ratio <= 1.0:
                print("Error: Summary ratio must be between 0.0 and 1.0.")
                sys.exit(1)
        except ValueError:
            print("Error: Summary ratio must be a number.")
            sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    # Generate the summary
    summary = summarize_text(text, ratio)
    original_sentences = len(re.split(r'(?<=[.!?])\s+', text.strip()))

    print("=" * 60)
    print(f"Text Summarization Report (Ratio: {ratio:.2f})")
    print("=" * 60)
    print(f"Original Text Sentence Count: {original_sentences}")
    print(f"Summary Sentence Count: {len(re.split(r'(?<=[.!?])\s+', summary.strip())) if summary and 'Error' not in summary else 'N/A'}")
    print("-" * 60)
    print("\n--- GENERATED SUMMARY ---\n")
    print(summary)
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
