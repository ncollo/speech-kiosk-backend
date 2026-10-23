import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

logger = logging.getLogger("clearcaption.db")

Base = declarative_base()

def get_engine():
    db_url = settings.DATABASE_URL
    try:
        if db_url.startswith("postgresql"):
            engine = create_engine(
                db_url,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
                connect_args={"connect_timeout": 3}
            )
            # Try a quick test connection
            with engine.connect() as conn:
                pass
            logger.info("Successfully connected to PostgreSQL database.")
            return engine
    except Exception as e:
        logger.warning(f"Could not connect to PostgreSQL at {db_url}: {e}")
        if settings.USE_SQLITE_FALLBACK:
            logger.warning("Falling back to local SQLite database: sqlite:///./clearcaption.db")
            return create_engine(
                "sqlite:///./clearcaption.db",
                connect_args={"check_same_thread": False}
            )
        raise

    return create_engine(
        db_url if not db_url.startswith("postgresql") else "sqlite:///./clearcaption.db",
        connect_args={"check_same_thread": False} if not db_url.startswith("postgresql") else {}
    )

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
