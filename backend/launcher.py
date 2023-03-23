'''
    Author: Andreas Neubauer

    Launcher of the flask app!
'''
# Imports from default libraries
import os

# Imports from the project
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = os.environ.get("FLASK_SERVER_PORT", 8000), debug=True)