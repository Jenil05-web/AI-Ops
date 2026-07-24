from triage.agents.triage_agent import TicketState

HIGH_RISK_QUEUES = {'Billing and Payments', 'Service Outages and Maintenance', 'Human Resources'}

def escalation_node(state:TicketState)->TicketState:
    """Flag tickets in high-risk queues for human review"""
    queue =state.get('predicted_queue')
    state['escalated'] = queue in HIGH_RISK_QUEUES
    return state

 