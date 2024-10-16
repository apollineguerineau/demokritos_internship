from model.stop_criteria.abstract_stop_criteria import AbstractStopCriteria

class NbRelevantStopCriteria(AbstractStopCriteria) :
    
    def __init__(self, nb_max_fetched) : 
        super().__init__( name=f'{nb_max_fetched} relevant pages fetched')
        self.nb_max_fetched = nb_max_fetched

    def is_reached(self, crawl_session):
        return(self.nb_max_fetched <= len(crawl_session.fetched_pages))