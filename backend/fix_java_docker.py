with open('app/services/judge.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '"java": "openjdk:17-slim"',
    '"java": "eclipse-temurin:17-jdk-jammy"'
)

with open('app/services/judge.py', 'w', encoding='utf-8') as f:
    f.write(content)
