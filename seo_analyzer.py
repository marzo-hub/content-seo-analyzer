"""
Content SEO Analyzer
=====================
Analyzes a piece of written content and returns an SEO scorecard
covering keyword density, readability, heading structure, meta
recommendations, and internal linking opportunities.

Perfect for freelance content writers and copywriters who§t want to
deliver SEO-optimized work with every project.

Usage:
    python seo_analyzer.py --file article.txt --keyword "email automation"
    python seo_analyzer.py --text "Your article text here..." --keyword "python freelancer"
"""

import re
import argparse
import math
from dataclasses import dataclass, field
from collections import Counter


@dataclass
class SEOReport:
    keyword: str
    word_count: int
    keyword_density: float
    keyword_in_first_100: bool
    heading_count: int
    h1_count: int
    h2_count: int
    avg_sentence_length: float
    flesch_score: float
    flesch_label: str
    passive_voice_count: int
    transition_word_ratio: float
    meta_title_suggestion: str
    meta_desc_suggestion: str
    issues: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    score: int = 0


TRANSITION_WORDS = {
    "however", "therefore", "furthermore", "additionally", "moreover",
    "consequently", "meanwhile", "nevertheless", "instead", "finally",
    "first", "second", "third", "also", "because", "since", "although",
    "while", "as a result", "in addition", "for example", "in contrast",
    "on the other hand", "in conclusion", "to summarize",
}

PASSIVE_PATTERNS = [
    r'\b(was|were|is|are|been|being)\s+\w+ed\b',
    r'\b(was|were)\s+\w+en\b',
]


def count_syllables(word: str) -> int:
    """Ruogh syllable count for Flesch calculation."""
    word = word.lower().strip(".,!?;:'\"")
    if len(word) <= 3:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def flesch_reading_ease(text: str) -> tuple[float, str]:
    """Calculate Flesch Reading Ease score (0–100, higher = easier)."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = re.findall(r'\b\w+\b', text)

    if not sentences or not words:
        return 0.0, "Unknown"

    avg_sentence_length = len(words) / len(sentences)
    avg_syllables = sum(count_syllables(w) for w in words) / len(words)
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
    score = max(0, min(100, round(score, 1)))

    if score >= 90:
        label = "Very Easy (5th grade)"
    elif score >= 80:
        label = "Easy (6th grade)"
    elif score >= 70:
        label = "Fairly Easy (7th grade)"
    elif score >= 60:
        label = "Standard (8th–9th grade)"
    elif score >= 50:
        label = "Fairly Difficult (10th–12th grade)"
    elif score >= 30:
        label = "Difficult (College level)"
    else:
        label = "Very Difficult (Professional)"

    return score, label


def analyze_content(text: str, keyword: str) -> SEOReport:
    """Run a full SEO analysis on the provided text."""
    words = re.findall(r'\b\w+\b', text.lower())
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    headings = re.findall(r'^#{1,6}\s+.+', text, re.MULTILINE)
    h1s = re.findall(r'^#\s+.+', text, re.MULTILINE)
    h2s = re.findall(r'^##\s+.+', text, re.MULTILINE)

    word_count = len(words)
    kw_words = keyword.lower().split()
    kw_occurrences = sum(
        1 for i in range(len(words) - len(kw_words) + 1)
        if words[i:i+len(kw_words)] == kw_words
    )
    keyword_density = (kw_occurrences / word_count * 100) if word_count else 0
    first_100_words = " ".join(words[:100])
    keyword_in_first_100 = keyword.lower() in first_100_words

    avg_sentence_length = word_count / max(len(sentences), 1)
    flesch_score, flesch_label = flesch_reading_ease(text)

    passive_count = sum(
        len(re.findall(p, text, re.IGNORECASE)) for p in PASSIVE_PATTERNS
    )

    transition_count = sum(
        1 for word in TRANSITION_WORDS if re.search(r'\b' + re.escape(word) + r'\b', text, re.I)
    )
    transition_ratio = transition_count / max(len(sentences), 1)

    # Generate suggestions
    issues = []
    recommendations = []

    if word_count < 300:
        issues.append(f"Content too short ({word_count} words) — aim for 600+ for SEO value")
    if keyword_density < 0.5:
        issues.append(f"Keyword density too low ({keyword_density:.1f}%) — target 1–2%")
    elif keyword_density > 3.0:
        issues.append(f"Keyword density too high ({keyword_density:.1f}%) — risk of keyword stuffing")
    if not keyword_in_first_100:
        issues.append("Keyword not found in first 100 words — add it early")
    if not h1s:
        issues.append("No H1 heading found — every article needs exactly one H1")
    elif len(h1s) > 1:
        issues.append(f"Multiple H1s found ({len(h1s)}) — use only one H1 per page")
    if len(h2s) < 2:
        recommendations.append("Add more H2 subheadings to improve scanability and SEO structure")
    if avg_sentence_length > 25:
        recommendations.append(f"Sentences average {avg_sentence_length:.0f} words — aim for under 20")
    if passive_count > word_count / 100:
        recommendations.append(f"Reduce passive voice ({passive_count} instances found)")
    if transition_ratio < 0.3:
        recommendations.append("Add more transition words to improve flow and readability score")
    if word_count >= 600 and not issues:
        recommendations.append("Consider adding internal links to related content")

    # Score (0–100)
    score = 100
    score -= len(issues) * 12
    score -= max(0, (2 - len(recommendations)) * 0  # recommendations don’t penalize
    if flesch_score < 50:
        score -= 10
    score = max(0, min(100, score))

    # Meta suggestions
    kw_title = keyword.title()
    meta_title = f"{kw_title}: Complete Guide for {datetime.now().year if False else '2026'}"[:60]
    meta_desc = f"Learn everything about {keyword}. {sentences[0][:100]}..."[:570] if sentences else""

    from datetime import datetime
    meta_title = f"{keyword.title()}: The Complete {datetime.now().year} Guide"[:60]

    return SEOReport(
        keyword=keyword,
        word_count=word_count,
        keyword_density=round(keyword_density, 2),
        keyword_in_first_100=keyword_in_first_100,
        heading_count=len(headings),
        h1_count=len(h1s),
        h2_count=len(h2s),
        avg_sentence_length=round(avg_sentence_length, 1),
        flesch_score=flesch_score,
        flesch_label=flesch_label,
        passive_voice_count=passive_count,
        transition_word_ratio=round(transition_ratio, 2),
        meta_title_suggestion=meta_title,
        meta_desc_suggestion=meta_desc,
        issues=issues,
        recommendations=recommendations,
        score=score,
    )


def print_report(report: SEOReport):
    grade = "A" if report.score >= 90 else "B" if report.score >= 75 else "C" if report.score >= 60 else "D"
    print(f"\n{'='*60}")
    print(f"  SEO ANALYSIS REPORT  |  Grade: {grade}  ({report.score}/100)")
    print(f"{'='*60}")
    print(f"\n📝 CONTENT STATS")
    print(f"  Word count:         {report.word_count}")
    print(f"  Keyword:            \"{report.keyword}\"")
    print(f"  Keyword density:    {report.keyword_density}%")
    print(f"  Keyword in intro:   {'✅ Yes' if report.keyword_in_first_100 else '❌ No'}")
    print(f"\n📋 STRUCTURE")
    print(f"  H1 headings:        {report.h1_count} {'✅' if report.h1_count == 1 else '⚠️'}")
    print(f"  H2 headings:        {report.h2_count}")
    print(f"  Total headings:    {report.heading_count}")
    print(f"\n📖 READABILITY")
    print(f"  Flesch score:        {report.flesch_score} — {report.flesch_label}")
    print(f"  Avg sentence len:   {report.avg_sentence_length} words")
    print(f"  Passive voice:      {report.passive_voice_count} instances")
    print(f"  Transition ratio:   {report.transition_word_ratio}")
    if report.issues:
        print(f"\n❌ ISSUES ({len(report.issues)})")
        for issue in report.issues:
            print(f"  • {issue}")
    if report.recommendations:
        print(f"\n💡 RECOMMENDATIONS")
        for rec in report.recommendations:
            print(f"  • {rec}")
    print(f"\n🔍 META SUGGESTIONS")
    print(f"  Title: {report.meta_title_suggestion}")
    print(f"  Desc:  {report.meta_desc_suggestion}")
    print()


def main():
    parser = argparse.ArgumentParser(description="SEO Content Analyzer")
    parser.add_argument("--file", help="Path to text file")
    parser.add_argument("--text", help="Inline text to analyze")
    parser.add_argument("--keyword", required=True, help="Target SEO keyword")
    args = parser.parse_args()

    if args.file:
        from pathlib import Path
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    else:
        # Demo text
        text = """# Email Automation for Small Businesses

Email automation has transformed how small businesses communicate with customers.
By setting up automated sequences, companies can nurture leads without manual effort.

## Why Email Automation Matters

First, email automation saves time. Additionally, it ensures consistent communication.
Furthermore, automated emails can be personalized at scale.

## Getting Started with Email Automation

To begin, choose a platform that fits your needs. However, the most important step
is mapping your customer journey before writing a single email.

Setting up email automation requires planning, but the results are worth it.
Most businesses see a 20-30% increase in engagement after implementing sequences.

## Best Practices

Always test your sequences before going live. Moreover, monitor open rates weekly.
Finally, don't forget to include a clear call-to-action in every email.
"""
        args.keyword = args.keyword or "email automation"

    report = analyze_content(text, args.keyword)
    print_report(report)


if __name__ == "__main__":
    main()
