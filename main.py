from models.database import init_db
init_db()
from models.database import db_session
from models.models import FeatureContent
db_session.commit()
