from agents.classification_agent import ClassificationAgent
def test_classification_basic(tmp_path):
    # create rules list
    rules = [
        {"docTypeCode":"INV","docTypeDescription":"Invoice","requiredKeywords":["invoice","total"], "optionalKeywords":["vendor"], "assumed":False, "regulatoryRiskFlags":[]},
        {"docTypeCode":"AGM","docTypeDescription":"Agreement","requiredKeywords":["agreement"], "optionalKeywords":["terms"], "assumed":False, "regulatoryRiskFlags":[]}
    ]
    c = ClassificationAgent(rules)
    res = c.run("This is an invoice with total amount and vendor details")
    assert res["docTypeCode"] == "INV"
