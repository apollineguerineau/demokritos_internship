from db.db_creation import TablePage, TableCrawlSession
from db.db_creation import session_page_association

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = "sqlite:///local_database.db"

class CrawlSessionDAO:
    def __init__(self):
        # Création de l'engine pour SQLAlchemy
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    def create_crawl_session(self, crawl_session, stop_criteria):
         # Démarre une session SQLAlchemy
        db_session = self.Session()

        db_crawl_session = TableCrawlSession(
                session_name=crawl_session.session_name,
                sorter=crawl_session.sorter.name,
                query_expander=crawl_session.query_expander.name,
                searcher=crawl_session.searcher.name,
                current_query=crawl_session.current_query,
                all_queries=crawl_session.all_queries,
                duration_time = str(datetime.now() - crawl_session.start_time),
                stop_criteria = stop_criteria.name
            )

        try:
            # Ajoute la session à la base de données
            db_session.add(db_crawl_session)
            db_session.commit()  # Sauvegarde temporaire pour générer l'ID de la session
            crawl_session.id = db_crawl_session.id

            for page in crawl_session.fetched_pages:
                # Vérifie si la page existe déjà en base, sinon, crée une nouvelle page
                db_page = db_session.query(TablePage).filter_by(url=page.url).first()

                if db_page is None:
                    db_page = TablePage(
                        url=str(page.url),
                        title=str(page.title),
                        description=str(page.description),
                        publication_date=str(page.publication_date),
                        authors=str(page.authors),
                        language=str(page.language),
                        notes=str(page.notes)
                    )
                    db_session.add(db_page)
                    db_session.commit()

                # Vérifie si le lien entre la session et la page existe déjà
                link_exists = db_session.execute(
                    session_page_association.select().where(
                        session_page_association.c.session_id == db_crawl_session.id,
                        session_page_association.c.page_id == db_page.id
                    )
                ).fetchone()

                # Si le lien n'existe pas, insère-le
                if link_exists is None:
                    is_seed = True
                    db_session.execute(
                        session_page_association.insert().values(
                            session_id=db_crawl_session.id,
                            page_id=db_page.id,
                            is_seed=is_seed,
                            score=page.score
                        )
                    )
            db_session.commit()

        
        except Exception as e:
            db_session.rollback()
            print(f"Erreur lors de l'enregistrement de la session de crawl : {e}")

        finally:
            db_session.close()

    
    def update_crawl_session(self, crawl_session):
        db_session = self.Session()

        try:
            db_crawl_session = db_session.query(TableCrawlSession).filter_by(id=crawl_session.id).first()

            if db_crawl_session:
                db_crawl_session.current_query = crawl_session.current_query
                db_crawl_session.all_queries = crawl_session.all_queries
                db_crawl_session.duration_time = str(datetime.now() - crawl_session.start_time)
                db_session.commit()
            else:
                print(f"La session de crawl avec l'ID {crawl_session.id} n'a pas été trouvée.")
            
            for page in crawl_session.fetched_pages:
                db_page = db_session.query(TablePage).filter_by(url=page.url).first()

                if db_page is None:
                    db_page = TablePage(
                        url=str(page.url),
                        title=str(page.title),
                        description=str(page.description),
                        publication_date=str(page.publication_date),
                        authors=str(page.authors),
                        language=str(page.language),
                        notes=str(page.notes)
                    )
                    db_session.add(db_page)
                    db_session.commit()

                # Vérifie si le lien entre la session et la page existe déjà
                link_exists = db_session.execute(
                    session_page_association.select().where(
                        session_page_association.c.session_id == crawl_session.id,
                        session_page_association.c.page_id == db_page.id
                    )
                ).fetchone()

                # Si le lien n'existe pas, insère-le
                if link_exists is None:
                    is_seed = False
                    db_session.execute(
                        session_page_association.insert().values(
                            session_id=crawl_session.id,
                            page_id=db_page.id,
                            is_seed=is_seed,
                            score=page.score
                        )
                    )
            db_session.commit()
                
        except Exception as e:
            db_session.rollback()
            print(f"Erreur lors de la mise à jour de la session de crawl : {e}")

        finally:
            db_session.close()

    def get_list_session_name_and_id(self):
        db_session = self.Session()
        try:
            # Récupère toutes les sessions avec leur ID et leur nom
            sessions = db_session.query(TableCrawlSession.id, TableCrawlSession.session_name).all()
            return [(session.id, session.session_name) for session in sessions]
        except Exception as e:
            print(f"Erreur lors de la récupération des sessions : {e}")
            return []
        finally:
            db_session.close()

    # Nouvelle fonction pour récupérer une session par son ID
    def get_session_by_id(self, session_id):
        db_session = self.Session()
        try:
            # Récupère la session correspondant à l'ID
            session = db_session.query(TableCrawlSession).filter_by(id=session_id).first()

            if session:
                # Récupère les pages associées à la session
                pages = db_session.query(TablePage).join(session_page_association).filter_by(session_id=session_id).all()
                return {
                    "session": session,
                    "pages": pages
                }
            else:
                print(f"Aucune session trouvée avec l'ID {session_id}")
                return None
        except Exception as e:
            print(f"Erreur lors de la récupération de la session : {e}")
            return None
        finally:
            db_session.close()


