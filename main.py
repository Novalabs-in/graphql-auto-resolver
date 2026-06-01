import sqlite3

class GraphqlAutoResolver:
    """
    Relational Schema Introspection GraphQL Generator
    Yields GraphQL Query schemas and type resolvers dynamically from database metadata.
    """
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")

    def introspect_schema(self):
        self.cursor.execute("PRAGMA table_info(users)")
        columns = self.cursor.fetchall()
        
        gql_type = "type User {\n"
        for col in columns:
            col_name, col_type = col[1], col[2]
            gql_field = f"  {col_name}: "
            gql_field += "Int" if col_type == "INTEGER" else "String"
            gql_type += gql_field + "\n"
        gql_type += "}"
        return gql_type

if __name__ == "__main__":
    resolver = GraphqlAutoResolver()
    print("Auto-Generated GraphQL Type Schema:")
    print(resolver.introspect_schema())
