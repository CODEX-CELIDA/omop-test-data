import tarfile
from pathlib import Path

import requests

GH_RELEASE_BASE = "https://github.com/CODEX-CELIDA/celida-recommendations/releases"
PACKAGE_NAME_TEMPLATE = (
    "recommendations.celida.codex.netzwerk-universitaetsmedizin.de-{version}.tgz"
)


def retrieve_latest_github_release() -> Path:
    """
    Retrieve the latest release of the guideline repository from GitHub.
    Returns: Path to the downloaded FHIR resources
    """
    base_path = Path("fhir-recommendations").absolute()

    base_path.mkdir(exist_ok=True)

    response = requests.get(GH_RELEASE_BASE + "/latest")
    if response.history:
        package_version = response.url.split("/")[-1]
        package_name = PACKAGE_NAME_TEMPLATE.format(version=package_version[1:])
    else:
        raise ValueError(
            "No redirect for recommendation URL, can't load latest package"
        )

    package_url = f"{GH_RELEASE_BASE}/download/{package_version}/{package_name}"

    r = requests.get(package_url, allow_redirects=True)
    with open(base_path / package_name, "wb") as f:
        f.write(r.content)

    tar = tarfile.open(base_path / package_name, "r:gz")
    tar.extractall(base_path)
    tar.close()

    return base_path / "package" / "example"


if __name__ == "__main__":
    retrieve_latest_github_release()
