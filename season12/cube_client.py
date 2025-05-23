import grpc
import logging
import cube_service_pb2
import cube_service_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO)

def run():
    """Run the gRPC client"""
    # Create a secure channel
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = cube_service_pb2_grpc.CubeServiceStub(channel)
        
        # Ask the user for input
        try:
            while True:
                try:
                    # Get user input
                    number = int(input("\nEnter a number to calculate its cube (or Ctrl+C to quit): "))
                    
                    # Log the request
                    logging.info(f"Sending request to calculate cube of {number}")
                    
                    # Make the gRPC call
                    response = stub.CalculateCube(cube_service_pb2.CubeRequest(number=number))
                    
                    # Display the result
                    print(f"📊 Result: The cube of {number} is {response.result}")
                    
                except ValueError:
                    print("❌ Error: Please enter a valid integer")
                except grpc.RpcError as e:
                    status_code = e.code()
                    print(f"❌ RPC Error: {status_code.name} - {e.details()}")
        
        except KeyboardInterrupt:
            print("\nExiting client")

if __name__ == "__main__":
    logging.info("Starting Cube Service client")
    run()