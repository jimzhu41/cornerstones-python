from app import db, create_app
from app.models import User, Roles
app=create_app()



@app.shell_context_processor
def make_shell_content():
    return {'db':db,'User':User,'Roles':Roles}





