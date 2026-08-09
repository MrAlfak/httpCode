import json
import tempfile
import unittest
from pathlib import Path
from httpcode import export_results, filter_items, load_codes, load_translations, localized_item

class TestHttpCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.codes=load_codes(); cls.en=load_translations("en")
    def test_dataset_has_v2_fields(self):
        required={"id","code","type","provider","phrase","description","class","status","source"}
        for item in self.codes: self.assertTrue(required.issubset(item))
    def test_search_by_standard_code(self): self.assertIn("iana-404",{x["id"] for x in filter_items(self.codes,"404",self.en)})
    def test_vendor_collision_is_preserved(self):
        ids={x["id"] for x in filter_items(self.codes,"530",self.en)}; self.assertIn("cloudflare-530",ids); self.assertIn("pantheon-530",ids)
    def test_provider_filter(self):
        results=filter_items(self.codes,"all",self.en,provider="aws-alb"); self.assertGreaterEqual(len(results),5); self.assertTrue(all(x["provider"]=="aws-alb" for x in results))
    def test_translated_search(self): self.assertTrue(any(x["code"]==404 for x in filter_items(self.codes,"پیدا نشد",load_translations("fa"))))
    def test_legacy_translation_only_applies_to_standard(self):
        tr={"530":{"phrase":"legacy","description":"legacy"}}; standard={"id":"iana-530","code":530,"type":"standard","phrase":"x","description":"y"}; vendor={"id":"cloudflare-530","code":530,"type":"vendor","phrase":"x","description":"y"}
        self.assertEqual(localized_item(standard,tr)["phrase"],"legacy"); self.assertEqual(localized_item(vendor,tr)["phrase"],"x")
    def test_json_export_is_localized(self):
        results=filter_items(self.codes,"404",load_translations("fa"))
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"out.json"; export_results(results,"json",out); data=json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data[0]["phrase"],"پیدا نشد")
    def test_invalid_language_raises(self):
        with self.assertRaises(ValueError): load_translations("definitely-not-a-language")
if __name__=="__main__": unittest.main()
