# Earthquake Research Project

Backend for a GIS web-app designed to generate insights from earthquake photos

## Installation on Bash Terminal

Clone the repository:

```bash
git clone https://github.com/alekszaf/EarthquakeMetadata.git
```

Navigate to the project directory:

```bash
cd EarthquakeMetadata
```

Create a virtual environment to keep the project dependencies isolated from your system Python:

```bash
python3.10.exe -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the dependencies for this project:

```bash
pip install .
```

## Installation on Windows PowerShell Terminal

Clone the repository:

```powershell
git clone https://github.com/alekszaf/EarthquakeMetadata.git
```

Navigate to the project directory:

```powershell
cd EarthquakeMetadata
```

Create a virtual environment to keep the project dependencies isolated from your system Python:

```powershell
python3.10.exe -m venv .venv
```

Activate the virtual environment

```powershell
.\.venv\Script\activate
```

Install the dependencies for this project:

```powershell
pip install .
```

Generate Google Cloud Platform (GCP) Service Account Key
The GIS web-app backend interacts with Google Cloud Platform services. You'll need to generate a service account key from GCP. Please follow these steps:

1. Go to the GCP Console: **https://console.cloud.google.com/.**
2. On the top-right corner, make sure you've selected the correct project for which you want to create the service account.
3. Navigate to **'IAM & Admin'** > **'Service Accounts'**.
4. Click on **Create Service Account** on the top of the page.
5. Enter the **'Service account name'** and **'Service account description'**, then click on **'CREATE'**.
6. Choose the roles for the service account as per your requirements and click on **'CONTINUE'**. For the EarthquakeMetadata project, you may need roles such as **'Storage Object Admin'**, **'BigQuery User'**, etc., depending on the specific GCP services the project interacts with.
7. (Optional) You can skip the **'Grant users access to this service account (optional)'** step unless you want other users to have access to this service account. Click on **'DONE'**.
8. On the Service Accounts page, find the newly created service account and click on the three-dot menu on the far right, then select **'Manage keys'**.
9. Click on **'ADD KEY'**, then **'Create new key'**.
10. Choose **'JSON'** as the **'Key type'**, then click on **'CREATE'**. The JSON key will be downloaded to your system.
Add Service Account Key to Project Directory
After you've downloaded the service account key, you need to move it to the correct directory in the project. Here is how you do it:

On Bash Terminal:

```bash
cd path/to/EarthquakeMetadata
mv /path/to/downloaded/key.json ./package/apis/loaders/google_cloud_platform/
```

On Windows PowerShell Terminal:

```powershell
cd /path/to/EarthquakeMetadata
Move-Item -Path path\to\downloaded\key.json -Destination .\package\apis\loaders\google_cloud_platform\
```

Please replace /path/to/downloaded/key.json or path\to\downloaded\key.json with the actual path where your downloaded service account key is located.

Now the service account key is in the right place, and the application will be able to use the GCP services as needed.