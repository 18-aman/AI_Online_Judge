from app.core.database import SessionLocal
from app.models.problem import Problem, Topic, ProblemTopic

db = SessionLocal()

def add_topics(title, topic_names):
    prob = db.query(Problem).filter(Problem.title == title).first()
    if not prob:
        return
    for t_name in topic_names:
        t = db.query(Topic).filter(Topic.name == t_name).first()
        if not t:
            t = Topic(name=t_name)
            db.add(t)
            db.commit()
            db.refresh(t)
        
        # Check if relation exists
        exists = db.query(ProblemTopic).filter(ProblemTopic.problem_id == prob.id, ProblemTopic.topic_id == t.id).first()
        if not exists:
            pt = ProblemTopic(problem_id=prob.id, topic_id=t.id)
            db.add(pt)
            db.commit()

add_topics('Two Sum', ['Array', 'Hash Table'])
add_topics('Valid Parentheses', ['String', 'Stack'])
add_topics('Contains Duplicate', ['Array', 'Hash Table'])
add_topics('Maximum Subarray', ['Array', 'Dynamic Programming', 'Divide and Conquer'])
add_topics('Best Time to Buy and Sell Stock', ['Array', 'Dynamic Programming'])
add_topics('Climbing Stairs', ['Dynamic Programming', 'Math'])
add_topics('Search Insert Position', ['Array', 'Binary Search'])
add_topics('Missing Number', ['Array', 'Bit Manipulation', 'Math'])

print('Topics seeded.')
