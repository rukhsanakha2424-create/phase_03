import traceback
from sqlmodel import Session
from app.db.session import get_session
from app.domain.todos.service import get_todos as db_get_todos

def test_get_todos():
    """Test if we can get todos from the database"""
    print("Testing get_todos function...")
    try:
        # Get a session
        session_gen = get_session()
        session = next(session_gen)
        
        # Call the get_todos function
        todos = db_get_todos(session)
        print(f"Successfully retrieved {len(todos)} todos from database")
        
        # Close the session
        session.close()
        print("Database session closed successfully")
        return True
    except Exception as e:
        print(f"Error in get_todos: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_get_todos()