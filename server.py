import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP Froid & Climatisation")


@mcp.tool()
def watts_vers_btu_h(watts: float) -> float:
    """Convertit des watts en BTU/h."""
    if watts < 0:
        raise ValueError("La puissance doit être positive.")

    return round(watts * 3.412141633, 2)


@mcp.tool()
def btu_h_vers_watts(btu_h: float) -> float:
    """Convertit des BTU/h en watts."""
    if btu_h < 0:
        raise ValueError("La puissance doit être positive.")

    return round(btu_h / 3.412141633, 2)


@mcp.tool()
def dimensionner_climatiseur(
    charge_thermique_w: float,
    marge_pct: float = 10
) -> dict:
    """Dimensionne un climatiseur à partir d'une charge thermique."""

    if charge_thermique_w <= 0:
        raise ValueError("La charge thermique doit être supérieure à zéro.")

    if not 0 <= marge_pct <= 50:
        raise ValueError("La marge doit être comprise entre 0 et 50 %.")

    charge_design = charge_thermique_w * (1 + marge_pct / 100)
    besoin_btu = charge_design * 3.412141633

    puissances = [
        9000,
        12000,
        18000,
        24000,
        30000,
        36000,
        48000,
        60000
    ]

    recommandation = next(
        (p for p in puissances if p >= besoin_btu),
        60000
    )

    if besoin_btu > 60000:
        remarque = (
            "Le besoin dépasse 60 000 BTU/h. "
            "Prévoir plusieurs unités ou un système adapté."
        )
    else:
        remarque = "Puissance commerciale recommandée."

    return {
        "charge_initiale_w": round(charge_thermique_w, 2),
        "marge_pct": marge_pct,
        "charge_design_w": round(charge_design, 2),
        "besoin_btu_h": round(besoin_btu, 2),
        "climatiseur_recommande_btu_h": recommandation,
        "remarque": remarque
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))

    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port
    )
