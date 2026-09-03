from sqlalchemy import create_engine
engine = create_engine('postgresql://admin:admin123@localhost:5432/online_judge')
with engine.connect() as con:
    rs = con.execute("SELECT id, title, difficulty FROM problems")
    probs = rs.fetchall()
    print("Problems:", probs)
    
    rs2 = con.execute("SELECT id, email FROM users")
    users = rs2.fetchall()
    print("Users:", users)
