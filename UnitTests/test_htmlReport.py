import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RSTAB.Reports.html import ExportResultTablesToHtml
from RSTAB.initModel import Model
from shutil import rmtree

if Model.clientModel is None:
    Model()

def test_html_report():
    Model.clientModel.service.delete_all()
    Model.clientModel.service.run_script('..\\scripts\\internal\\Demos\\Demo-001 Hall.js')
    Model.clientModel.service.calculate_all(False)

    dirname = os.path.join(os.getcwd(), os.path.dirname(__file__))
    # Remove any previous results if they exist
    folderPath = os.path.join(dirname, 'testResults')
    if os.path.isdir(folderPath):
        rmtree(folderPath)
    ExportResultTablesToHtml(folderPath)

    assert os.path.exists(folderPath)
