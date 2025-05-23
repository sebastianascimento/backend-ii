import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional, Dict

# ----- Sample Data -----
# In-memory user database
USERS = {
    1: {"id": 1, "name": "Sebastian Nascimento", "email": "sebastian@example.com"},
    2: {"id": 2, "name": "Alice Johnson", "email": "alice@example.com"},
    3: {"id": 3, "name": "Bob Smith", "email": "bob@example.com"}
}

# ----- GraphQL Types -----
@strawberry.type
class User:
    id: int
    name: str
    email: str

# ----- Input Types -----
@strawberry.input
class UpdateNameInput:
    id: int
    name: str

# ----- Query Type -----
@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        """Get a user by ID"""
        user_data = USERS.get(id)
        if user_data:
            return User(**user_data)
        return None
    
    @strawberry.field
    def users(self) -> List[User]:
        """Get all users"""
        return [User(**user) for user in USERS.values()]

# ----- Mutation Type -----
@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_user_name(self, input: UpdateNameInput) -> Optional[User]:
        """Update a user's name"""
        user_id = input.id
        new_name = input.name
        
        # Check if the user exists
        if user_id not in USERS:
            return None
        
        # Update the user's name
        USERS[user_id]["name"] = new_name
        
        # Return the updated user
        return User(**USERS[user_id])

# ----- FastAPI Integration -----
# Create schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create a GraphQL router
graphql_router = GraphQLRouter(schema)

# Create the FastAPI app
app = FastAPI(title="User GraphQL API")

# Add the GraphQL route
app.include_router(graphql_router, prefix="/graphql")

# Add a redirect from the root to the GraphiQL interface
@app.get("/")
async def redirect_to_graphql():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("user_api:app", host="0.0.0.0", port=8000, reload=True)