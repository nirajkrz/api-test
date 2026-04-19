import json
import os
from typing import Dict, Any, List

class ResultPublisher:
    """Publishes test execution results in various formats."""

    def __init__(self, results: List[Dict[str, Any]], output_dir: str):
        self.results = results
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def publish_results(self):
        """Publishes test results in JSON and HTML formats."""
        self._publish_json()
        self._publish_html()

    def _publish_json(self):
        """Publishes test results in JSON format."""
        json_path = os.path.join(self.output_dir, 'results.json')
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=2)

    def _publish_html(self):
        """Publishes test results in HTML format."""
        html_path = os.path.join(self.output_dir, 'results.html')
        html_content = self._generate_html_content()
        with open(html_path, 'w') as f:
            f.write(html_content)

    def _generate_html_content(self) -> str:
        """Generates HTML content for the test report."""
        passed_count = sum(1 for r in self.results if r['passed'])
        failed_count = len(self.results) - passed_count
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .summary {{ margin-bottom: 20px; }}
                .summary p {{ margin: 5px 0; }}
                .passed {{ color: green; }}
                .failed {{ color: red; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .details {{ display: none; margin-top: 10px; padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd; }}
                .toggle-details {{ cursor: pointer; color: blue; text-decoration: underline; }}
            </style>
            <script>
                function toggleDetails(id) {{
                    var details = document.getElementById(id);
                    if (details.style.display === "none") {{
                        details.style.display = "block";
                    }} else {{
                        details.style.display = "none";
                    }}
                }}
            </script>
        </head>
        <body>
            <h1>API Test Report</h1>
            <div class="summary">
                <p>Total Tests: {len(self.results)}</p>
                <p class="passed">Passed: {passed_count}</p>
                <p class="failed">Failed: {failed_count}</p>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Test Case</th>
                        <th>Type</th>
                        <th>Method</th>
                        <th>URL</th>
                        <th>Status</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
        """
        for i, result in enumerate(self.results):
            status_class = "passed" if result['passed'] else "failed"
            status_text = "Passed" if result['passed'] else "Failed"
            html += f"""
                    <tr>
                        <td>{result['name']}</td>
                        <td>{result['type']}</td>
                        <td>{result['method']}</td>
                        <td>{result['url']}</td>
                        <td class="{status_class}">{status_text}</td>
                        <td>
                            <span class="toggle-details" onclick="toggleDetails('details-{i}')">View Details</span>
                            <div id="details-{i}" class="details">
                                <p><strong>Parameters:</strong> {json.dumps(result['parameters'], indent=2)}</p>
                                <p><strong>Request Body:</strong> {json.dumps(result['request_body'], indent=2)}</p>
                                <p><strong>Expected Status:</strong> {result['expected_status']}</p>
                                <p><strong>Actual Status:</strong> {result['actual_status']}</p>
                                <p><strong>Response Body:</strong> <pre>{result['response_body']}</pre></p>
                            </div>
                        </td>
                    </tr>
            """
        html += """
                </tbody>
            </table>
        </body>
        </html>
        """
        return html
