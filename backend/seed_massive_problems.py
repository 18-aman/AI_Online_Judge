from app.core.database import SessionLocal
from app.models.problem import Problem, TestCase, Difficulty
import uuid

db = SessionLocal()

problems = [
    {
        "title": "Maximum Subarray",
        "description": "Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return *its sum*.\n\n**Example 1:**\n```\nInput: nums = [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6\nExplanation: [4,-1,2,1] has the largest sum = 6.\n```\n\n**Example 2:**\n```\nInput: nums = [1]\nOutput: 1\n```",
        "difficulty": Difficulty.MEDIUM,
        "time_limit": 2.0,
        "memory_limit": 256.0,
        "testcases": [
            ("[-2, 1, -3, 4, -1, 2, 1, -5, 4]", "6", False),
            ("[1]", "1", False),
            ("[5, 4, -1, 7, 8]", "23", True),
            ("[-1, -2, -3]", "-1", True)
        ]
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "description": "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.\n\nYou want to maximize your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock.\n\nReturn *the maximum profit you can achieve from this transaction*. If you cannot achieve any profit, return `0`.\n\n**Example 1:**\n```\nInput: prices = [7,1,5,3,6,4]\nOutput: 5\nExplanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.\n```",
        "difficulty": Difficulty.EASY,
        "time_limit": 2.0,
        "memory_limit": 128.0,
        "testcases": [
            ("[7, 1, 5, 3, 6, 4]", "5", False),
            ("[7, 6, 4, 3, 1]", "0", False),
            ("[1, 2]", "1", True),
            ("[2, 4, 1]", "2", True)
        ]
    },
    {
        "title": "Climbing Stairs",
        "description": "You are climbing a staircase. It takes `n` steps to reach the top.\n\nEach time you can either climb `1` or `2` steps. In how many distinct ways can you climb to the top?\n\n**Example 1:**\n```\nInput: n = 2\nOutput: 2\nExplanation: There are two ways to climb to the top.\n1. 1 step + 1 step\n2. 2 steps\n```\n\n**Example 2:**\n```\nInput: n = 3\nOutput: 3\nExplanation: There are three ways to climb to the top.\n1. 1 step + 1 step + 1 step\n2. 1 step + 2 steps\n3. 2 steps + 1 step\n```",
        "difficulty": Difficulty.EASY,
        "time_limit": 1.0,
        "memory_limit": 128.0,
        "testcases": [
            ("2", "2", False),
            ("3", "3", False),
            ("4", "5", True),
            ("45", "1836311903", True)
        ]
    },
    {
        "title": "Search Insert Position",
        "description": "Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.\n\nYou must write an algorithm with `O(log n)` runtime complexity.\n\n**Example 1:**\n```\nInput: nums = [1,3,5,6]\n5\nOutput: 2\n```\n\n**Example 2:**\n```\nInput: nums = [1,3,5,6]\n2\nOutput: 1\n```",
        "difficulty": Difficulty.EASY,
        "time_limit": 1.5,
        "memory_limit": 128.0,
        "testcases": [
            ("[1, 3, 5, 6]\n5", "2", False),
            ("[1, 3, 5, 6]\n2", "1", False),
            ("[1, 3, 5, 6]\n7", "4", True),
            ("[1, 3, 5, 6]\n0", "0", True)
        ]
    },
    {
        "title": "Missing Number",
        "description": "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return *the only number in the range that is missing from the array*.\n\n**Example 1:**\n```\nInput: nums = [3,0,1]\nOutput: 2\nExplanation: n = 3 since there are 3 numbers, so all numbers are in the range [0,3]. 2 is the missing number in the range since it does not appear in nums.\n```\n\n**Example 2:**\n```\nInput: nums = [0,1]\nOutput: 2\n```",
        "difficulty": Difficulty.EASY,
        "time_limit": 1.5,
        "memory_limit": 128.0,
        "testcases": [
            ("[3, 0, 1]", "2", False),
            ("[0, 1]", "2", False),
            ("[9, 6, 4, 2, 3, 5, 7, 0, 1]", "8", True),
            ("[0]", "1", True)
        ]
    }
]

for p_data in problems:
    if db.query(Problem).filter(Problem.title == p_data["title"]).first():
        continue
    p = Problem(
        id=uuid.uuid4(),
        title=p_data["title"],
        description=p_data["description"],
        difficulty=p_data["difficulty"],
        time_limit=p_data["time_limit"],
        memory_limit=p_data["memory_limit"]
    )
    db.add(p)
    db.commit()
    
    for inp, out, hidden in p_data["testcases"]:
        tc = TestCase(
            id=uuid.uuid4(),
            problem_id=p.id,
            input_data=inp,
            expected_output=out,
            is_hidden=hidden
        )
        db.add(tc)
    db.commit()

print("Massive problem batch seeded successfully!")

