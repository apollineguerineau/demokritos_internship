from stop_criteria.abstract_stop_criteria import AbstractStopCriteria

class NbRelevantStopCriteria(AbstractStopCriteria) :
    
    def __init__(self, crawl_session, nb_max_fetched) : 
        super().__init__(crawl_session, name=f'{nb_max_fetched} relevant pages fetched')
        self.nb_max_fetched = nb_max_fetched

    def is_reached(self):
        return(self.nb_max_fetched <= len(self.crawl_session.fetched_pages))