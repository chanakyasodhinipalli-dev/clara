from agents.splitter_agent import SplitterAgent
from agents.context_agent import ContextAgent
from agents.grouping_agent import GroupingAgent
from agents.classification_agent import ClassificationAgent
from agents.summary_agent import SummaryAgent

class AgentRegistry:
    def __init__(self, config, context_model):
        self.agents = {
            "splitter": SplitterAgent(config),
            "context": ContextAgent(context_model),
            "grouping": GroupingAgent(),
            "classification": ClassificationAgent(config),
            "summary": SummaryAgent()
        }

    def get_agent(self, name):
        return self.agents.get(name)
