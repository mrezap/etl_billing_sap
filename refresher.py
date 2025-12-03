import subprocess
from concurrent.futures import ThreadPoolExecutor
from config import PBI_SCRIPTS
from logger import logger

def run_refresh_pbi(logger):
    def _run(script):
        try:
            subprocess.run(
                ["python", script],
                check=True, capture_output=True, text=True
            )
            logger.info(f"Triger successful: {script}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Triger failed: {script} - {e}")

    with ThreadPoolExecutor() as pool:
        pool.map(_run, PBI_SCRIPTS)
