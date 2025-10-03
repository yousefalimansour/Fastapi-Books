import asyncio
import asyncpg
from src.config import settings

async def view_database():
    try:
        # Parse the DATABASE_URL to get connection parameters
        # postgresql+asyncpg://postgres:postgres@localhost:5432/books_db
        url = settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://')
        
        conn = await asyncpg.connect(url)
        
        # List all databases
        print("=== Available Databases ===")
        databases = await conn.fetch("SELECT datname FROM pg_database WHERE datistemplate = false;")
        for db in databases:
            print(f"- {db['datname']}")
        
        print("\n=== Current Database Info ===")
        current_db = await conn.fetchval("SELECT current_database();")
        print(f"Connected to database: {current_db}")
        
        # List all tables in current database
        print(f"\n=== Tables in '{current_db}' ===")
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        
        if tables:
            for table in tables:
                print(f"- {table['table_name']}")
        else:
            print("No tables found in the database.")
        
        # Check if books table exists and show its structure
        books_table = await conn.fetch("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'books' AND table_schema = 'public'
            ORDER BY ordinal_position;
        """)
        
        if books_table:
            print(f"\n=== Structure of 'books' table ===")
            for col in books_table:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                default = f"DEFAULT {col['column_default']}" if col['column_default'] else ""
                print(f"- {col['column_name']}: {col['data_type']} {nullable} {default}")
            
            # Show data in books table
            book_data = await conn.fetch("SELECT * FROM books LIMIT 10;")
            if book_data:
                print(f"\n=== Data in 'books' table (first 10 rows) ===")
                for book in book_data:
                    print(dict(book))
            else:
                print(f"\n=== Data in 'books' table ===")
                print("No data found in the books table.")
        
        await conn.close()
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL server is running")
        print("2. Database 'books_db' exists")
        print("3. User 'postgres' has access to the database")

if __name__ == "__main__":
    asyncio.run(view_database())