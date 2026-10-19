import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from data_access import REGIONS, load_region, select_rows, annual_totals


class DashboardTest(unittest.TestCase):
    def test_snapshot_and_filters(self):
        expected = {"IATTC": 339300, "ICCAT": 8592, "IOTC": 13500}
        for region in REGIONS:
            data = load_region(region)
            self.assertEqual(len(data), expected[region])
            rows = select_rows(data, "BLUE SHARK", 2020)
            self.assertFalse(rows.empty)
            self.assertTrue(rows.year.eq(2020).all())
            self.assertTrue(rows.species_commonname.eq("BLUE SHARK").all())
            self.assertAlmostEqual(annual_totals(data)["catch"].sum(), data["catch"].sum(), places=4)
            self.assertTrue(select_rows(data, "NONEXISTENT", 2020).empty)

    def test_ui_region_species_year_and_layer(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=45).run()
        self.assertFalse(app.exception)
        for region in REGIONS:
            app.selectbox[0].select(region).run()
            self.assertFalse(app.exception)
            app.selectbox[1].select(app.selectbox[1].options[-1]).run()
            app.select_slider[0].set_value(2012).run()
            app.radio(key="layer").set_value("Original model prediction").run()
            app.radio(key="trend_scope").set_value("Selected species").run()
            self.assertFalse(app.exception)


if __name__ == "__main__":
    unittest.main()
