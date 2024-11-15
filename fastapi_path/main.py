from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from example_pb2_grpc import LibraryStub
from example_pb2 import Request
import grpc
import copy
import uvicorn

app = FastAPI()

st_response_json = {
    'status': 'error',
    'err_description': '',
    'book_title': ''
}

class BookData(BaseModel):
    id: int = Field(default=1)

@app.post('/', name='', tags=['No API'], description='', response_class=JSONResponse, status_code=200)
def _request(bookData: BookData):
    response_json = copy.deepcopy(st_response_json)
    
    try:
        with grpc.insecure_channel('localhost:5001') as channel:
            stub = LibraryStub(channel)
            request = stub.Book(Request(id=bookData.id))
        
        if request.HasField('success'):
            response_json['book_title'] = request.success.title
        elif request.HasField('fail'):
            response_json['err_description'] = request.fail.description
    
    except (Exception, ) as e:
        response_json['err_description'] = str(e)
        
    finally:
        return JSONResponse(
            content=response_json
        )
    
if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)
