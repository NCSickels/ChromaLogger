"""Usage example"""

from chromalogger import ChromaLogger


def main() -> None:
    # Create a logger instance
    logger = ChromaLogger()
    logger.get_logger()

    # Set the logging level
    logger.setLevel(10)

    # Log messages
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")


if __name__ == "__main__":
    main()
