from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = "sqlite:///local_database.db"

# BDD initialization
Base = declarative_base()

# Association table for many-to-many relationship between Expert and Page
expert_page_association = Table(
    'expert_page', Base.metadata,
    Column('expert_id', Integer, ForeignKey('experts.id'), primary_key=True),
    Column('page_id', Integer, ForeignKey('pages.id'), primary_key=True),
    Column('is_relevant', Boolean)  # Optional rating provided by the expert for a page
)

# Association table for many-to-many relationship between CrawlSession and Page
# Each page can be marked as a "seed" (and therefore automatically "fetched").
session_page_association = Table(
    'session_page', Base.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True),
    Column('page_id', Integer, ForeignKey('pages.id'), primary_key=True),
    Column('is_seed', Boolean, default=False),
    Column('score', Float) 
)

# Page table
class TablePage(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    publication_date = Column(String)
    authors = Column(String)
    language = Column(String) 
    notes = Column(String)

    # Many-to-many relationship with CrawlSession
    sessions = relationship('TableCrawlSession', secondary=session_page_association, back_populates='pages')

    # Many-to-many relationship with Expert
    experts = relationship('TableExpert', secondary=expert_page_association, back_populates='pages')

    def __repr__(self):
        return f"<Page(id={self.id}, url={self.url}, title={self.title})>"

# CrawlSession table
class TableCrawlSession(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True) 
    session_name = Column(String, nullable=False)
    sorter = Column(String)
    query_expander = Column(String)
    searcher = Column(String)
    current_query = Column(String)
    all_queries = Column(String)
    stop_criteria = Column(String)
    duration_time = Column(String)

    # Many-to-many relationship with Page
    pages = relationship('TablePage', secondary=session_page_association, back_populates='sessions')

    def __repr__(self):
        return f"<CrawlSession(id={self.id}, session_name={self.session_name})>"

# Expert table
class TableExpert(Base):
    __tablename__ = 'experts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 

    # Many-to-many relationship with Page
    pages = relationship('TablePage', secondary=expert_page_association, back_populates='experts')

    def __repr__(self):
        return f"<Expert(id={self.id}, name={self.name})>"

# Create the database and tables
def create_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database and tables created.")

if __name__ == "__main__":
    create_database()
