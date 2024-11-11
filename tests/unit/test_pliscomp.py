from src.pliscomp.main import main
from click.testing import CliRunner
import os


def test_simplest_for_loop_case():
   runner = CliRunner()
   result = runner.invoke(main, [os.path.abspath("tests/data/for_loop_simplest_case.py")])
   assert "new_list = [item for item in stuff]\n" == result.stdout
