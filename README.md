# Service with referral system (template)
### Written with FastAPI.
---
> :warning: To run this service, you must manually setup environment and database (PostgreSQL) on your machine.

### How to use:
1. Set up .env file (check env_example for more info).
2. Run these commands:
   
   ```shell script
   make install
   make deploy
   ```
3. Use http://localhost/docs from browser to access Swagger UI.

### Requirements (stack):
- Python ^3.10
- Poetry
- PostgreSQL ^14
- SQLAlchemy
- Alembic
- JWT, OAuth2.0
