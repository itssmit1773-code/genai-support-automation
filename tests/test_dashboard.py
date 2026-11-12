from pathlib import Path
import unittest

try:
    from streamlit.testing.v1 import AppTest
except ImportError:
    AppTest = None


@unittest.skipIf(AppTest is None, "Install dashboard requirements to run UI tests")
class DashboardTests(unittest.TestCase):
    def test_dashboard_loads_and_controls_recalculate(self):
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(app_path), default_timeout=60).run()
        self.assertFalse(app.exception)
        self.assertEqual([tab.label for tab in app.tabs],
                         ["Operations", "Quality", "Risk", "Financial scenarios"])
        baseline = app.tabs[3].get("html")[0].proto.body
        app.tabs[0].selectbox[0].select("APAC")
        app.tabs[1].selectbox[0].select("risk")
        app.tabs[2].selectbox[0].select("Prompt injection")
        app.tabs[3].slider[0].set_value(7000)
        app.run()
        self.assertFalse(app.exception)
        self.assertNotEqual(app.tabs[0].metric[0].value, "12,000")
        self.assertEqual(app.tabs[2].selectbox[0].value, "Prompt injection")
        changed = app.tabs[3].get("html")[0].proto.body
        self.assertIn("$11,709", baseline)
        self.assertNotIn("$11,709", changed)

