from os import getenv

import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        app='src.app:app',
        host='0.0.0.0',
        port=int(getenv('BACK_URL').split(':')[2]),
    )
