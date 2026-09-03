from app.core.database import SessionLocal
from app.models.problem import Problem

db = SessionLocal()
problems = db.query(Problem).all()

schemas = {
    'Two Sum': {
        'function_name': 'twoSum',
        'return_type': 'list<integer>',
        'parameters': [
            {'name': 'nums', 'type': 'list<integer>'},
            {'name': 'target', 'type': 'integer'}
        ]
    },
    'Valid Parentheses': {
        'function_name': 'isValid',
        'return_type': 'boolean',
        'parameters': [{'name': 's', 'type': 'string'}]
    },
    'Contains Duplicate': {
        'function_name': 'containsDuplicate',
        'return_type': 'boolean',
        'parameters': [{'name': 'nums', 'type': 'list<integer>'}]
    },
    'Maximum Subarray': {
        'function_name': 'maxSubArray',
        'return_type': 'integer',
        'parameters': [{'name': 'nums', 'type': 'list<integer>'}]
    },
    'Best Time to Buy and Sell Stock': {
        'function_name': 'maxProfit',
        'return_type': 'integer',
        'parameters': [{'name': 'prices', 'type': 'list<integer>'}]
    },
    'Climbing Stairs': {
        'function_name': 'climbStairs',
        'return_type': 'integer',
        'parameters': [{'name': 'n', 'type': 'integer'}]
    },
    'Search Insert Position': {
        'function_name': 'searchInsert',
        'return_type': 'integer',
        'parameters': [
            {'name': 'nums', 'type': 'list<integer>'},
            {'name': 'target', 'type': 'integer'}
        ]
    },
    'Missing Number': {
        'function_name': 'missingNumber',
        'return_type': 'integer',
        'parameters': [{'name': 'nums', 'type': 'list<integer>'}]
    }
}

for p in problems:
    if p.title in schemas:
        p.signature_schema = schemas[p.title]

db.commit()
print('Migration complete.')
