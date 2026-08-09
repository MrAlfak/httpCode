import subprocess
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent
class TestDataQuality(unittest.TestCase):
    def test_validator(self):
        completed=subprocess.run([sys.executable,str(ROOT/"tools"/"validate.py")],cwd=ROOT,text=True,capture_output=True); self.assertEqual(completed.returncode,0,completed.stdout+completed.stderr)
    def test_generated_dataset_is_clean(self):
        before=(ROOT/"codes.json").read_text(encoding="utf-8"); completed=subprocess.run([sys.executable,str(ROOT/"tools"/"build_dataset.py")],cwd=ROOT,text=True,capture_output=True); self.assertEqual(completed.returncode,0,completed.stdout+completed.stderr); after=(ROOT/"codes.json").read_text(encoding="utf-8"); self.assertEqual(before,after)
if __name__=="__main__": unittest.main()
