import logging
import sys
import os
from datetime import datetime

def setup_logging(log_file='application.log', console_level=logging.INFO, file_level=logging.DEBUG):
    """
    Set up logging configuration with both file and console handlers.
    
    Args:
        log_file (str): Path to the log file
        console_level: Minimum level for console output
        file_level: Minimum level for file output
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all levels
    
    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s - %(message)s'
    )
    
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(file_level)
    file_handler.setFormatter(file_formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def simulate_application_flow():
    """Simulate various application scenarios that generate different log levels."""
    
    logging.debug("Starting application initialization...")
    
    # Simulate configuration loading - DEBUG level
    logging.debug("Loading configuration from config.json")
    
    # Simulate successful startup - INFO level
    logging.info("Application started successfully")
    logging.info(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Simulate user authentication
        username = "sebastian"
        logging.info(f"User {username} logged in")
        
        # Simulate potential security concern - WARNING level
        logging.warning("Multiple failed login attempts detected from IP 192.168.1.5")
        
        # Simulate processing some data
        process_data()
        
        # Simulate an error condition
        division_by_zero()
        
    except Exception as e:
        # Log the exception - ERROR level
        logging.error(f"An error occurred during execution: {str(e)}", exc_info=True)
    
    finally:
        # Simulate application shutdown - INFO level
        logging.info("Application shutting down")

def process_data():
    """Simulate data processing with various log levels."""
    logging.debug("Starting data processing routine")
    
    # Simulate processing steps
    records_processed = 1000
    logging.info(f"Successfully processed {records_processed} records")
    
    # Simulate a warning condition
    duplicate_records = 5
    if duplicate_records > 0:
        logging.warning(f"Found {duplicate_records} duplicate records in the dataset")
    
    logging.debug("Data processing completed")

def division_by_zero():
    """Function that will cause a division by zero error."""
    logging.debug("Performing critical calculation")
    
    # This will raise a ZeroDivisionError
    result = 10 / 0
    return result

def main():
    """Main function to demonstrate logging."""
    # Set up logging
    setup_logging(
        log_file='logs/application.log',
        console_level=logging.INFO,  # Console shows INFO and above
        file_level=logging.DEBUG     # File captures all levels including DEBUG
    )
    
    logging.info("=" * 50)
    logging.info("LOGGING DEMONSTRATION STARTED")
    logging.info("=" * 50)
    
    # Log messages at different levels directly
    logging.debug("This is a DEBUG message - for detailed diagnostic information")
    logging.info("This is an INFO message - for confirmation that things are working")
    logging.warning("This is a WARNING message - for potential issues that might need attention")
    logging.error("This is an ERROR message - for problems that need to be addressed")
    logging.critical("This is a CRITICAL message - for serious errors that may lead to program termination")
    
    # Simulate application flow with various log levels
    simulate_application_flow()
    
    logging.info("=" * 50)
    logging.info("LOGGING DEMONSTRATION COMPLETED")
    logging.info("=" * 50)

if __name__ == "__main__":
    main()