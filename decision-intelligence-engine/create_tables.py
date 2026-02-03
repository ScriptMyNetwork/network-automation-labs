from app.database import engine, Base
from app.models import Decision

Base.metadata.create_all(bind=engine)
print("Decision table created")
