from concurrent import futures
import grpc
import logging
import cube_service_pb2
import cube_service_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)

class CubeServicer(cube_service_pb2_grpc.CubeServiceServicer):
    """Implementation of the CubeService service"""
    
    def CalculateCube(self, request, context):
        """
        Calculate the cube of the requested number
        
        Args:
            request: The request containing the number
            context: The gRPC context
            
        Returns:
            A CubeResponse with the calculated result
        """
        number = request.number
        logging.info(f"Received request to calculate cube of {number}")
        
        # Calculate the cube
        result = number ** 3
        
        logging.info(f"Returning cube result: {result}")
        return cube_service_pb2.CubeResponse(result=result)

def serve():
    """Start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cube_service_pb2_grpc.add_CubeServiceServicer_to_server(CubeServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.info("Starting Cube Service server")
    serve()