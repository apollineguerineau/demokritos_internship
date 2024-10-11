from db.db_creation import TablePage, TableCrawlSession
from db.db_creation import session_page_association

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from datetime import datetime

# Assurez-vous que DATABASE_URL est correctement configurée
DATABASE_URL = "sqlite:///local_database.db"

class CrawlSessionDAO:
    def __init__(self):
        # Création de l'engine pour SQLAlchemy
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    def save_crawl_session(self, crawl_session, stop_criteria):
        """
        Enregistre la session de crawl et les pages liées dans la base de données.
        client_crawler: une instance de ClientCrawler qui contient la session de crawl à sauvegarder.
        """
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
     
            # Traite les pages fetched
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

                if page in crawl_session.seed_pages : 
                    is_seed = 1
                else :
                    is_seed = 0
                # Ajoute la relation entre la session et la page (qui est également récupérée)
                db_session.execute(
                    session_page_association.insert().values(
                        session_id=db_crawl_session.id,
                        page_id=db_page.id,
                        is_seed=is_seed  # Indique que ce n'est pas une page seed
                    )
                )
            db_session.commit()

        except Exception as e:
            db_session.rollback()
            print(f"Erreur lors de l'enregistrement de la session de crawl : {e}")

        finally:
            db_session.close()


