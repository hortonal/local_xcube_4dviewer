# Running DeepESDL's xcube and 4D Viewer Locally

This repository provides a lightweight template for hosting your own **xcube Server** and integrating it with the **xcube 4D Viewer plugin**, allowing you to visualize data in the [4dviewer.com](https://4dviewer.com) web application.

## Using This Repository

This repo includes a **Docker container** and a **VSCode development container configuration**, making it easy to get started.

### Quick Start

1. Clone this repository locally.
2. Open the folder in a new VSCode instance.
3. Use the VSCode menu to run:
   **"Dev Containers: Open Folder in Container"**

> ⚠️ Ensure that a local Docker daemon (e.g., Docker Desktop) is running.

Once the container has been built, start all services from a terminal instance with:

```bash
python run_locally.py
```

This will:

* Launch all required services
* Provide a clickable URL to open the local 4D Viewer
* Host example xcube data from the `/xcube-server-data` directory

The resulting URL will look similar to:

``` sh
Web viewer available at: http://localhost:5003/?gateway=http%3A%2F%2Flocalhost%3A5001%2Fapi-v1
```

In the web application, the example data is available under **Data Browser → example_data**.

---

## Official DeepESDL 4D Viewer Documentation

For detailed guidance on using the 4D Viewer web application user interface, see:
[https://earthsystemdatalab.net/guide/visualisation/4d-viewer/](https://earthsystemdatalab.net/guide/visualisation/4d-viewer/)

---

## Generating xcube Data

This repository includes an example of publishing xcube-compatible data under the `/generating_example_data` folder.

* Any xcube dataset supporting levels should work if `xcube server` can serve the data.
* You may need to update `xcube_server_config.yml` to add or modify data sources.
* For more information, see the official xcube documentation: [https://xcube.readthedocs.io/en/latest/](https://xcube.readthedocs.io/en/latest/)/.
