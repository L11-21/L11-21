from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class InvestmentProduct:
    name: str
    what: str
    risk: str
    typical_return: str
    liquidity: str
    use_case: str

INVESTMENT_PRODUCTS = [
    InvestmentProduct(
        name="ETF",
        what="Basket of assets traded like a stock.",
        risk="Moderate",
        typical_return="5–10% annually for equity ETFs",
        liquidity="High",
        use_case="Diversification, growth exposure, easy entry into markets"
    ),
    InvestmentProduct(
        name="CD",
        what="Bank deposit locked for a fixed term with guaranteed interest.",
        risk="Low",
        typical_return="3–5% depending on term",
        liquidity="Low",
        use_case="Safe parking of cash, predictable returns"
    ),
    InvestmentProduct(
        name="Treasury Securities",
        what="U.S. government bonds (bills, notes, bonds).",
        risk="Very Low",
        typical_return="3–5% depending on maturity",
        liquidity="Moderate",
        use_case="Stability, safe haven, balancing risk in portfolio"
    ),
    InvestmentProduct(
        name="Commodity Futures",
        what="Contracts to buy/sell commodities at a set future price.",
        risk="High",
        typical_return="Highly variable, leveraged gains/losses",
        liquidity="Moderate",
        use_case="Hedging, speculation, advanced strategies"
    )
]

RISK_TO_MEME = {
    "Very Low": "🥱🛡️",       # ultra-safe snooze
    "Low": "😐💤",            # sleepy safety
    "Moderate": "🤔🎢",       # thoughtful rollercoaster
    "High": "🔥🙃🚀"           # fire, upside-down, rocket
}

RISK_LEVELS = {"Very Low": 1, "Low": 2, "Moderate": 4, "High": 8}

def memeify_investment(product: InvestmentProduct) -> Dict[str, Any]:
    """Turn an investment product into a 'meme' summary, encoding risk as an integer for quant/AI use."""
    risk_emoji = RISK_TO_MEME.get(product.risk, "❓")
    loss_magnitude = RISK_LEVELS.get(product.risk, 0)
    meme = f"{product.name}: {risk_emoji} Risk={product.risk} | {product.typical_return} | Tip: {product.use_case}"
    return {
        "name": product.name,
        "meme": meme,
        "loss_magnitude": loss_magnitude
    }

def feed_losses_to_qubits(products: List[InvestmentProduct], cubit_counter: "CubitCounter"):
    """
    Feed the 'losses' (from risk levels) into the CubitCounter system.
    Returns a mapping from product to its snapped proportional magnitude.
    """
    output = {}
    for prod in products:
        meme_data = memeify_investment(prod)
        snap = cubit_counter.snap_to_nearest_ratio(meme_data["loss_magnitude"])
        output[prod.name] = {
            "meme": meme_data["meme"],
            "loss_level": meme_data["loss_magnitude"],
            "snapped_qubit": snap
        }
    return output

# ----------------
# Usage Example:
#
# Add this block within your main() *after* CubitCounter is initialized:
# (Assume: cubits = CubitCounter(base_unit=1.0))
#
#   memes = feed_losses_to_qubits(INVESTMENT_PRODUCTS, cubits)
#   for name, info in memes.items():
#       logging.info("Meme for %s: %s | Qubit: %s", name, info["meme"], info["snapped_qubit"])
# ----------------
