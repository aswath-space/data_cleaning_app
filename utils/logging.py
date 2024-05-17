import logging

def setup_logging(log_file='app.log'):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler()
                        ])
    logging.info("Logging setup complete.")

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)
