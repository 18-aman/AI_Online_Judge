import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import json

np.random.seed(42)
num_records = 5000

user_success_rate = np.random.uniform(0.2, 0.9, num_records)
user_skill_tier = np.random.choice([1, 2, 3], num_records, p=[0.5, 0.3, 0.2])
problem_difficulty = np.random.choice([1, 2, 3], num_records, p=[0.5, 0.3, 0.2])
problem_pass_rate = np.random.uniform(0.1, 0.9, num_records)

probabilities = user_success_rate * 0.4 + problem_pass_rate * 0.4
difficulty_gap = problem_difficulty - user_skill_tier
probabilities = np.where(difficulty_gap > 0, probabilities - (difficulty_gap * 0.25), probabilities)
probabilities = np.where(difficulty_gap < 0, probabilities + 0.15, probabilities)
probabilities = np.clip(probabilities, 0, 1)

will_solve = np.random.binomial(1, probabilities)

df = pd.DataFrame({
    'user_success_rate': user_success_rate,
    'user_skill_tier': user_skill_tier,
    'problem_difficulty': problem_difficulty,
    'problem_pass_rate': problem_pass_rate,
    'will_solve': will_solve
})

X = df.drop('will_solve', axis=1)
y = df['will_solve']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=4,
    random_state=42,
    eval_metric='logloss'
)

print("Training XGBoost Recommendation Model...")
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.4f}")

model.save_model("recommendation_model.json")
print("Model saved to recommendation_model.json!")
