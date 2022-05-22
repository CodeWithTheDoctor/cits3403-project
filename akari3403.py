from app import db, cli, create_app, oauth
from app.main import routes
from app.models import User, Puzzle, User_Puzzle
from config import Config


app = create_app()
cli.register(app)

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "config": Config,
        "Puzzle": Puzzle,
        "User_Puzzle": User_Puzzle,
        "routes": routes,
    }
