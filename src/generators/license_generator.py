import requests
from .base import BaseGenerator


class LicenseGenerator(BaseGenerator):
    def _get_cc_license_text(self, license_type):
        """Generate Creative Commons license text"""
        contributors = self.config.get("contributors", [])
        copyright_holder = (
            contributors[0]["name"] if contributors else "Copyright Holder"
        )
        year = (
            self.config.get("published", "").split("-")[0]
            if self.config.get("published")
            else "2024"
        )
        title = self.config.get("title", "This work")

        cc_licenses = {
            "cc0-1.0": f"""CC0 1.0 Universal (CC0 1.0) Public Domain Dedication

{copyright_holder} has dedicated the work "{title}" to the public domain by waiving all of his or her rights to the work worldwide under copyright law, including all related and neighboring rights, to the extent allowed by law.

You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

For more information, see: https://creativecommons.org/publicdomain/zero/1.0/""",
            "cc-by-4.0": f"""Creative Commons Attribution 4.0 International Public License

Copyright (c) {year} {copyright_holder}

This work is licensed under the Creative Commons Attribution 4.0 International License.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

For the full license text, see: https://creativecommons.org/licenses/by/4.0/""",
            "cc-by-sa-4.0": f"""Creative Commons Attribution-ShareAlike 4.0 International Public License

Copyright (c) {year} {copyright_holder}

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

For the full license text, see: https://creativecommons.org/licenses/by-sa/4.0/""",
            "cc-by-nc-4.0": f"""Creative Commons Attribution-NonCommercial 4.0 International Public License

Copyright (c) {year} {copyright_holder}

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- NonCommercial — You may not use the material for commercial purposes.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

For the full license text, see: https://creativecommons.org/licenses/by-nc/4.0/""",
            "cc-by-nc-sa-4.0": f"""Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License

Copyright (c) {year} {copyright_holder}

This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- NonCommercial — You may not use the material for commercial purposes.
- ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

For the full license text, see: https://creativecommons.org/licenses/by-nc-sa/4.0/""",
        }

        return cc_licenses.get(license_type)

    def generate(self):
        license_type = self.config.get("license", "").lower()

        # Check if it's a Creative Commons license
        if license_type.startswith("cc"):
            cc_text = self._get_cc_license_text(license_type)
            if cc_text:
                return cc_text
            else:
                return f"""Creative Commons License

This work is licensed under the {license_type.upper()} Creative Commons License.

For the full license text, please visit: {self.config.get('license_url', f'https://creativecommons.org/licenses/{license_type.replace("cc-", "").replace("-", "/")}')}"""

        # Get GitHub license template for software licenses
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
