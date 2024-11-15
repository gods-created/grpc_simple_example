from example_pb2_grpc import LibraryStub
from example_pb2 import Request
import grpc

def run(id: str) -> str:
    message = ''
            
    try:
        with grpc.insecure_channel('localhost:5001') as channel:
            stub = LibraryStub(channel)
            response = stub.Book(Request(id=int(id)))

        if response.HasField('success'):
            message = f'Book title: \'{response.success.title}\'.'
        elif response.HasField('fail'):
            message = f'Error: {response.fail.description.lower()}.'
        else:
            message = f'Error: gRPC server not answers.'
    
    except (Exception, ) as e:
        message = str(e).lower()
        
    finally:
        return message
        
if __name__ == '__main__':
    try:
        id = input('BOOK ID: ')
        print(
            run(id)
        )
        
    except (KeyboardInterrupt, Exception, ) as e:
        print(str(e))
