from concurrent import futures
from example_pb2_grpc import LibraryServicer, add_LibraryServicer_to_server
from library import books
from example_pb2 import Reply, SuccessReply, FailReply
import grpc

class LibraryServicer(LibraryServicer):
    def Book(self, request, context) -> Reply:
        try:
            id = request.id
            book = books.get(id, {})
            if book:
                return Reply(
                    success=SuccessReply(
                        title=book.get('title', 'No name')
                    )
                )
            else:
                return Reply(
                    fail=FailReply(
                        description=book.get('description', 'Book didn\'t find!')
                    )
                )
        
        except (Exception, ) as e:
            print(str(e))
        
        
def run() -> None:
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_LibraryServicer_to_server(LibraryServicer(), server)
        server.add_insecure_port('[::]:5001')
        server.start()
        server.wait_for_termination()
    
    except (Exception, ) as e:
        print(str(e))
        
if __name__ == '__main__':
    try:
        run()
        
    except (KeyboardInterrupt, Exception, ) as e:
        print(str(e))
