import os
from celery import Celery
from app.core.database import SessionLocal
from app.models.problem import Problem
from app.models.submission import Submission
from app.services.judge import run_code_in_docker

celery_app = Celery(
    "online_judge_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(name="execute_submission")
def execute_submission(submission_id: str):
    db = SessionLocal()
    try:
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            return
            
        submission.status = "RUNNING"
        db.commit()
        
        problem = submission.problem
        test_cases = problem.test_cases
        
        # Execute the code inside Docker
        result = run_code_in_docker(
            language=submission.language,
            code=submission.code,
            test_cases=test_cases,
            time_limit=problem.time_limit,
            custom_checker_code=problem.checker_code if problem.has_custom_checker else None,
            signature_schema=problem.signature_schema
        )
        
        # Update submission with results
        submission.status = "COMPLETED"
        submission.verdict = result["status"]
        submission.results = result["results"]
        db.commit()
        
    except Exception as e:
        db.rollback()
        # In case of catastrophic failure
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if submission:
            submission.status = "FAILED"
            submission.verdict = "Internal Error"
            db.commit()
    finally:
        db.close()
