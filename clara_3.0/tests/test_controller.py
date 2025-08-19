from api.controller import run_pipeline
import os
def test_controller_smoke(tmp_path):
    # create a tiny pdf with PyMuPDF
    import fitz
    doc = fitz.open()
    for i in range(2):
        page = doc.new_page()
        page.insert_text((72,72), f"Test page {i+1} invoice total 100")
    fp = tmp_path/"sample.pdf"
    doc.save(str(fp))
    doc.close()
    out = run_pipeline(str(fp))
    assert "groups" in out
    assert isinstance(out["groups"], list)
