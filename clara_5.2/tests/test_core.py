from pathlib import Path
from core.orchestrator import Orchestrator

def test_workflows_load(tmp_path):
    app_dir = Path(__file__).resolve().parents[1]
    orch = Orchestrator(app_dir)
    assert 'full_pipeline' in orch.workflows

def test_splitter_single_pdf(tmp_path):
    app_dir = Path(__file__).resolve().parents[1]
    test_pdf = tmp_path / "one.pdf"
    # Create a single-page pdf
    from reportlab.pdfgen import canvas
    test_pdf.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(test_pdf))
    c.drawString(100, 750, "Hello Page 1")
    c.showPage()
    c.save()

    orch = Orchestrator(app_dir)
    from agents.splitter_agent import SplitterAgent
    agent = SplitterAgent(orch.ctx, {})
    out = agent.run(test_pdf)
    assert out['documents']
    assert Path(out['documents'][0]['path']).exists()

def test_metadata_extraction(tmp_path):
    app_dir = Path(__file__).resolve().parents[1]
    test_pdf = tmp_path / "meta.pdf"
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    c = canvas.Canvas(str(test_pdf), pagesize=A4)
    c.drawString(50, 800, "Name: John Doe")
    c.drawString(50, 780, "PAN: ABCDE1234F")
    c.drawString(50, 760, "Account: 123456789012")
    c.save()

    orch = Orchestrator(app_dir)
    from agents.metadata_extraction_agent import MetadataAgent
    agent = MetadataAgent(orch.ctx, {})
    out = agent.run(test_pdf)
    assert out['metadata']['pan'] == 'ABCDE1234F'
