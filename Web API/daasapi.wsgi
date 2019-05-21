import sys
import warnings

sys.path.insert(0, '/var/www/daas')
warnings.filterwarnings("ignore")

from server import app as application
