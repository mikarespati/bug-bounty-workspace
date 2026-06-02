import os
from dotenv import load_dotenv
from app import create_app, db

load_dotenv()

app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Target': __import__('app.models', fromlist=['Target']).Target,
        'Note': __import__('app.models', fromlist=['Note']).Note,
        'Endpoint': __import__('app.models', fromlist=['Endpoint']).Endpoint,
        'Finding': __import__('app.models', fromlist=['Finding']).Finding,
    }


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )