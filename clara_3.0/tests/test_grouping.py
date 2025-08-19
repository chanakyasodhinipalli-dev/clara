import numpy as np
from agents.grouping_agent import GroupingAgent

def test_grouping_simple():
    # create fake pages with embeddings in metadata
    pages = [
        {"page_number":1, "text":"alpha", "embedding":[1.0,0.0,0.0]},
        {"page_number":2, "text":"alpha content", "embedding":[0.98,0.05,0.01]},
        {"page_number":3, "text":"beta", "embedding":[0.0,1.0,0.0]}
    ]
    g = GroupingAgent()
    groups = g.run(pages)
    assert len(groups) == 2
    # one group should have 2 pages, other 1
    sizes = sorted([len(x) for x in groups])
    assert sizes == [1,2]
