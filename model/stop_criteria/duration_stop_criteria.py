from model.stop_criteria.abstract_stop_criteria import AbstractStopCriteria
from datetime import datetime, timedelta

class DurationStopCriteria(AbstractStopCriteria) :
    
    def __init__(self, maximum_duration) : 
        super().__init__( name=f'{maximum_duration} minutes')
        self.maximum_duration = timedelta(minutes=maximum_duration)

    def is_reached(self, crawl_session):
        return(self.maximum_duration < datetime.now() - crawl_session.start_time)