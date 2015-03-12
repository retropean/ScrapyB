from sqlalchemy.orm import sessionmaker
from models import Fares, db_connect, create_fares_table

#class ScrapybPipeline(object):
#    def process_item(self, item, spider):
#        return item

class ScrapybPipeline(object):
    """Livingsocial pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_fares_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        fare = Fares(**item)

        try:
            session.add(fare)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item