import requests
from .base import BaseGenerator


class LicenseGenerator(BaseGenerator):
    def generate(self):
        license_type = self.config.get("license", "").lower()

        # Get GitHub license template
        try:
            url = f"https://api.github.com/licenses/{license_type}"
            response = requests.get(url)
            response.raise_for_status()

            license_data = response.json()
            license_body = license_data.get("body", "")

            # Replace placeholders with your info
            contributors = self.config.get("contributors", [])
            copyright_holder = (
                contributors[0]["name"] if contributors else "Copyright Holder"
            )
            year = (
                self.config.get("published", "").split("-")[0]
                if self.config.get("published")
                else "2024"
            )

            # Replace common placeholders
            license_body = license_body.replace("[year]", year)
            license_body = license_body.replace("[fullname]", copyright_holder)
            license_body = license_body.replace(
                "[name of copyright owner]", copyright_holder
            )
            license_body = license_body.replace("[yyyy]", year)
            license_body = license_body.replace("[name of author]", copyright_holder)

            return license_body

        except requests.RequestException:
            return f"""Error: Could not fetch license template for '{license_type}'

GitHub supports many licenses including:
- Common: mit, apache-2.0, gpl-3.0, lgpl-3.0, mpl-2.0
- BSD variants: bsd-2-clause, bsd-3-clause, bsd-3-clause-clear  
- Creative Commons: cc0-1.0, cc-by-4.0, cc-by-sa-4.0, cc-by-nc-sa-4.0
- Others: agpl-3.0, unlicense, isc

For the complete list, see: https://docs.github.com/en/rest/licenses
Or visit: {self.config.get('license_url', '')}"""
