from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv

load_dotenv()

def get_company_symbol(company: str) -> str:
    """Use this function to get the symbol for a company.
    Args:
        company (str): The name of the company.
    Returns:
        str: The symbol for the company.
    """
    symbols = {
        "Phidata": "MSFT",
        "Infosys": "INFY",
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "Google": "GOOGL"
    }
    
    return symbols.get(company, "Unknown")

# DDGo
web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.1-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

# Financial Agent
finance_agent = Agent(
    name="FinGen",
    model=Groq(id="llama-3.1-70b-versatile"),
    tools=[YFinanceTools(stock_price =True, analyst_recommendations=True, stock_fundamentals=True), get_company_symbol],
    show_tool_calls=True,
    markdown=True,
    instructions=[
        "Use tables to display numbers related data.", 
        "Consider yourself as a financial assistant named 'FinGen(Financial Genesis)', answer to question accordingly",
        "If you get wrong response (i.e <function=get_current_stock_price{'symbol': 'NVDA'}), try to call the functions again and come back with better response.",
        ],
    debug_mode=True
)

agent_team = Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="llama-3.1-70b-versatile"),
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True
)

prompt = input("Ask FinGen: ")

while prompt!= "exit":
    agent_team.print_response(prompt)
    prompt = input("Ask FinGen: ")
