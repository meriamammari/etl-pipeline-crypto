import argparse
import asyncio
import logging
import signal
import time
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETLPipeline:
    async def deploy_ci_cd(self) -> Dict[str, str]:
        logger.info("Starting CI/CD pipeline setup...")
        await asyncio.sleep(1)  # Simulate async operation
        logger.info("CI/CD pipeline setup completed.")
        return {"status": "success", "message": "Task Setup CI/CD pipeline completed successfully"}

    async def setup_monitoring(self) -> Dict[str, str]:
        logger.info("Starting monitoring and alerting setup...")
        await asyncio.sleep(1)  # Simulate async operation
        logger.info("Monitoring and alerting setup completed.")
        return {"status": "success", "message": "Task Setup monitoring & alerting completed successfully"}

    async def create_runbook(self) -> Dict[str, str]:
        logger.info("Starting deployment runbook creation...")
        await asyncio.sleep(1)  # Simulate async operation
        logger.info("Deployment runbook creation completed.")
        return {"status": "success", "message": "Task Create deployment runbook completed successfully"}

async def main(config: str, dry_run: bool, phase: str) -> int:
    pipeline = ETLPipeline()
    start_time = time.time()
    exit_code = 0

    try:
        if phase == "deployment":
            tasks = [
                pipeline.deploy_ci_cd(),
                pipeline.setup_monitoring(),
                pipeline.create_runbook()
            ]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result["status"] != "success":
                    exit_code = 2
                    logger.error(result["message"])
                else:
                    logger.info(result["message"])
        else:
            logger.warning("No valid phase provided. Exiting with partial success.")
            exit_code = 1

    except Exception as e:
        logger.exception("An error occurred during the ETL process.")
        exit_code = 2

    duration = time.time() - start_time
    logger.info(f"Execution completed in {duration:.2f} seconds with exit code {exit_code}.")
    return exit_code

def signal_handler(sig, frame):
    logger.info("Graceful shutdown initiated.")
    asyncio.get_event_loop().stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL Pipeline Entry Point")
    parser.add_argument("--config", type=str, required=True, help="Path to the configuration file")
    parser.add_argument("--dry-run", action="store_true", help="Run the pipeline in dry run mode")
    parser.add_argument("--phase", type=str, required=True, help="Specify the phase to execute")

    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    exit_code = asyncio.run(main(args.config, args.dry_run, args.phase))
    exit(exit_code)