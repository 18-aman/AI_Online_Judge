with open('app/api/recommendations.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '"match_score": round(final_score * 100, 1), "win_probability": round(raw_prob * 100, 1)',
    '"match_score": float(round(final_score * 100, 1)), "win_probability": float(round(raw_prob * 100, 1))'
)

with open('app/api/recommendations.py', 'w', encoding='utf-8') as f:
    f.write(content)
