# Content SEO Analyzer

A Python CLI tool that analyzes written content and produces a detailed SEO scorecard — built for freelance writers and copywriters who want to deliver measurably optimized work.

## What It Checks

| Category | Metrics |
|----------|---------|
| **Keyword** | Density, placement in intro, natural usage |
| **Structure** | H1/H2 count, heading hierarchy |
| **Readability** | Flesch Reading Ease, avg sentence length |
| **Style** | Passive voice count, transition word ratio |
| **Meta** | Auto-generated title & description suggestions |

## Quick Start

```bash
pip install -r requirements.txt

# Analyze a file
python seo_analyzer.py --file my_article.txt --keyword "email automation"

# Analyze inline text
python seo_analyzer.py --text "Your article here..." --keyword "python freelancer"

# Run built-in demo
python seo_analyzer.py --keyword "email automation"
```

## Example Output

```
============================================================
  SEO ANALYSIS REPORT  |  Grade: B  (78/100)
============================================================

📝 CONTENT STATS
  Word count:         542
  Keyword:            "email automation"
  Keyword density:    1.3%
  Keyword in intro:   ✅ Yes

📋 STRUCTURE
  H1 headings:        1 ✅
  H2 headings:        3
  Total headings:     4

📖 READABILITY
  Flesch score:       68.2 — Fairly Easy (7th grade)
  Avg sentence len:   16.4 words
  Passive voice:      2 instances

❌ ISSUES (0)

💡 RECOMMENDATIONS
  • Add more transition words to improve flow

🔍 META SUGGESTIONS
  Title: Email Automation: The Complete 2026 Guide
  Desc:  Learn everything about email automation...
```

## Grading Scale

| Grade | Score | Meaning |
|-------|-------|----------|
| A | 90–100 | Publication ready |
| B | 75–89 | Minor improvements needed |
| C | 60–74 | Significant revisions recommended |
| D | 0V$�59 | Major SEO issues present |

## License

MIT
