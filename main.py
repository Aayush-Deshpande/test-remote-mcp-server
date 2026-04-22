from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
                  CREATE TABLE IF NOT EXISTS expenses(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category TEXT NOT NULL,
                  subcategory TEXT DEFAULT ' ',
                  note TEXT DEFAULT ' '
                  )
                  """)
        
init_db()

@mcp.tool()
def add_expenses(date, amount, category, subcategory="", note=""):
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("INSERT INTO expenses (date, amount, category, subcategory, note) VALUES (?, ? ,?, ?, ?)", 
                        (date, amount, category, subcategory, note))
        return {"status": "ok", "id": cur.lastrowid}

@mcp.tool()
def list_expenses(start_date, end_date):
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY id ASC", (start_date, end_date))   
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    
@mcp.tool()
def summarize_expenses(start_date, end_date, category=None):
    with sqlite3.connect(DB_PATH) as c:
        query = ("""
                SELECT CATEGORY, SUM(amount) AS Total_amount
                FROM expenses
                WHERE DATE BETWEEN ? AND ?
                """)
        params = [start_date, end_date]

        if category != None:
            query += "AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC "

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

if __name__ == "__main__":
    import uvicorn
    from starlette.middleware.cors import CORSMiddleware

    app = mcp.http_app()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)