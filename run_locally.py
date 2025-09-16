#!/usr/bin/env python3
import subprocess
import time
import json
import requests
import urllib.parse
import os
import sys


# ----------------------------
# Configuration
# ----------------------------
folder = "."
gateway_url = "http://0.0.0.0:5001"
xcube_url = "http://0.0.0.0:8889"


# ----------------------------
# Helper Functions
# ----------------------------
def service_is_up(url) -> bool:
    """Check if an HTTP service is up."""
    try:
        return requests.get(url).ok
    except requests.exceptions.ConnectionError:
        return False


def start_subprocess(cmd):
    """Start a subprocess in the background and return the Popen object."""
    return subprocess.Popen(cmd)


def wait_for_service(url, name):
    """Wait until a service is up."""
    print(f"Waiting for {name} to start...")
    while not service_is_up(url):
        print(f"{name} not running. Retrying...")
        time.sleep(1)
    print(f"{name} running.")


# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    try:
        # Start services
        xcube_file = os.path.join(folder, "xcube_server_config.yml")
        xcube_cmd = ["xcube", "serve", "--port", "8889",
                     "--config", xcube_file, "--verbose"]
        gateway_cmd = ["gunicorn", "--bind", ":5001", "--workers", "1",
                       "--threads", "16", "--timeout", "0",
                       "gateway_4d_viewer.__main__:app"]
        nginx_cmd = ["nginx"]

        print("Starting services...")

        xcube_proc = start_subprocess(xcube_cmd)
        gateway_proc = start_subprocess(gateway_cmd)
        nginx_proc = start_subprocess(nginx_cmd)

        # Wait for services to become available
        wait_for_service(f"{gateway_url}/api-v1/configurations",
                         "Gateway server")
        wait_for_service(f"{xcube_url}/", "Xcube server")

        # Register xcube server with gateway
        print("Registering xcube server with the gateway...")
        payload = {
            "data_source_type": "xcube_server_data_source",
            "server_url": "http://127.0.0.1:8889/4d_viewer"
        }
        response = requests.post(
            f"{gateway_url}/register-data-source/xcube_source",
            data=json.dumps(payload))
        if response.ok:
            print("Successfully registered local xcube server.")

        # Clean up unwanted datasources
        for ds in ["ESDL", "XCUBE-DEV"]:
            requests.delete(f"{gateway_url}/deregister-data-source/{ds}")

        # Construct web viewer URL
        host = "http://localhost:"
        gateway_external_url = host + "5001/api-v1"
        viewer_client_url = f"{host}5003/?gateway={
            urllib.parse.quote(gateway_external_url, safe='')}"

        print(f"Web viewer available at: {viewer_client_url}")

        print("All services running. Press Ctrl-C to stop.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping all services...")

        # Terminate all subprocesses
        for proc in [xcube_proc, gateway_proc, nginx_proc]:
            if proc.poll() is None:  # still running
                proc.terminate()  # sends SIGTERM
        for proc in [xcube_proc, gateway_proc, nginx_proc]:
            if proc.poll() is None:
                proc.wait()
        print("All services stopped. Exiting.")
        sys.exit(0)
