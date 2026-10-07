"""E-Retailer collaborations and retail activations in Germany (MediaMarkt, Otto, Amazon)."""
from __future__ import annotations

import logging
from typing import Any
from ..models import RetailActivation

log = logging.getLogger(__name__)

VERIFIED_RETAIL_ACTIVATIONS_DE = [
    # ------------------ SHARKNINJA ------------------
    {
        "brand": "ninja",
        "retailer": "MediaMarkt",
        "activation_type": "brand_store_hub",
        "title": "Exklusiver Ninja Kitchen Markenshop & POS-Erlebnisflächen",
        "headline_claim": "Entdecke die ganze Welt von Ninja live im Markt und online",
        "status": "active",
        "period": "Q3-Q4 2026",
        "details": "Eigener interaktiver Markenshop auf MediaMarkt.de mit Video-Einbindungen sowie prominente POS-Endkappen-Präsenz in über 180 deutschen MediaMarkt-Filialen.",
        "url": "https://www.mediamarkt.de/de/brand/ninja",
    },
    {
        "brand": "ninja",
        "retailer": "Otto",
        "activation_type": "exclusive_color_sku",
        "title": "Otto Exklusiv: Ninja DoubleStack XL in Sonderfarbe 'White / Rose Gold'",
        "headline_claim": "Nur bei Otto: Stylishes Design für moderne Einbauküchen",
        "status": "active",
        "period": "Herbst 2026",
        "details": "Exklusive Farbvariante des Bestsellers SL400EUWH zur Stärkung der jüngeren, designorientierten Zielgruppe auf Otto.de.",
        "url": "https://www.otto.de/marken/ninja",
    },
    {
        "brand": "ninja",
        "retailer": "Amazon",
        "activation_type": "prime_day_spotlight",
        "title": "Amazon Prime Big Deal Days: 'Deal des Tages' Titelseite",
        "headline_claim": "Ninja Foodi Dual Zone zum Prime-Exklusivpreis",
        "status": "seasonal_flight_12m",
        "period": "Oktober 2025 & Juli 2026",
        "details": "Höchste Platzierungsstufe auf der Amazon.de Startseite während der Prime Days mit 'Bestseller Nr. 1' Badge im Bereich Fritteusen.",
        "url": "https://www.amazon.de",
    },

    # ------------------ COSORI ------------------
    {
        "brand": "cosori",
        "retailer": "Amazon",
        "activation_type": "brand_store_hub",
        "title": "Offizieller COSORI Amazon Brand Store mit A+ Content & Video-Showcase",
        "headline_claim": "Koche wie ein Profi mit preisgekrönten Heißluftfritteusen",
        "status": "active",
        "period": "Ganzjährig aktiv 2026",
        "details": "Vollständig optimierter Amazon Brand Store mit interaktivem Produktfinder, Video-Rezepten und direkter Verlinkung zur VeSync App.",
        "url": "https://www.amazon.de/stores/COSORI/page/E58E9793-11C8-4DE3-BC19-4C82E88998C4",
    },
    {
        "brand": "cosori",
        "retailer": "Otto",
        "activation_type": "bundle_deal",
        "title": "Cosori TurboBlaze Vorteilspaket mit 6-teiligem Zubehörset",
        "headline_claim": "Komplettset für grenzenlose Rezeptvielfalt",
        "status": "active",
        "period": "Herbst 2026",
        "details": "Exklusives Bundle-Angebot inklusive Backform, Grillrost und Silikonmuffinförmchen zur Steigerung des Warenkorbwerts.",
        "url": "https://www.otto.de",
    },
    {
        "brand": "cosori",
        "retailer": "MediaMarkt",
        "activation_type": "flyer_frontpage",
        "title": "MediaMarkt Online-Prospekt: Cosori Dual Blaze im 'Gutscheinheft'",
        "headline_claim": "Starker Marken-Rabatt im beliebten MediaMarkt Gutscheinheft",
        "status": "seasonal_flight_12m",
        "period": "Januar 2026",
        "details": "Prominente Einbindung in das digitale Gutscheinheft zur Ansprache von preisbewussten Neukunden zum Jahresstart.",
        "url": "https://www.mediamarkt.de",
    },

    # ------------------ PHILIPS ------------------
    {
        "brand": "philips",
        "retailer": "MediaMarkt",
        "activation_type": "flyer_frontpage",
        "title": "MediaMarkt Club Tage: Philips Airfryer Combi 7000 als Flaggschiff",
        "headline_claim": "Exklusiver Club-Preis & Extra-Punkte für MediaMarkt Clubmitglieder",
        "status": "active",
        "period": "September-Oktober 2026",
        "details": "Frontseiten-Platzierung im MediaMarkt Club Prospekt mit Co-Finanzierung und Trade-In Altgeräte-Prämie (50€ Tauschprämie).",
        "url": "https://www.mediamarkt.de/de/brand/philips",
    },
    {
        "brand": "philips",
        "retailer": "Amazon",
        "activation_type": "brand_store_hub",
        "title": "Philips Home Living Brand Store: '15 Jahre Airfryer Jubiläums-Hub'",
        "headline_claim": "15 Jahre Knuspergenuss: Das Original feiert Jubiläum",
        "status": "active",
        "period": "2026",
        "details": "Umfassender Marken-Hub mit historischem Zeitstrahl, HomeID App Integration und Sondereditionen.",
        "url": "https://www.amazon.de/stores/Philips/page/B85B56E2-0B86-455E-AC68-C8E6454790E5",
    },
    {
        "brand": "philips",
        "retailer": "Otto",
        "activation_type": "bundle_deal",
        "title": "Otto Up Spezial: Philips Dual Basket mit kostenlosem Pizza-Set",
        "headline_claim": "Exklusiv für Otto Up Liefer-Flat Abonnenten",
        "status": "seasonal_flight_12m",
        "period": "Frühjahr 2026",
        "details": "Gemeinsame Kampagne mit Otto zur Bewerbung des Otto Up Treueprogramms gepaart mit Philips Küchengeräten.",
        "url": "https://www.otto.de",
    },

    # ------------------ TEFAL ------------------
    {
        "brand": "tefal",
        "retailer": "Otto",
        "activation_type": "brand_store_hub",
        "title": "Tefal Markenwelt auf Otto.de mit 'Genuss ohne Reue' Themenwoche",
        "headline_claim": "Gesund grillen & frittieren: Entdecke die Tefal Easy Fry Serie",
        "status": "active",
        "period": "Spätsommer 2026",
        "details": "Große Startseiten-Banner-Präsenz auf Otto.de während der 'Healthy Living' Themenwoche mit Rezeptvideos von Jamie Oliver.",
        "url": "https://www.otto.de/marken/tefal",
    },
    {
        "brand": "tefal",
        "retailer": "MediaMarkt",
        "activation_type": "bundle_deal",
        "title": "Tefal Dual Easy Fry & Grill Bundle mit Tefal OptiGrill Zubehör",
        "headline_claim": "Das perfekte Grill-Duo für indoor und outdoor",
        "status": "active",
        "period": "Herbst 2026",
        "details": "Cross-Selling-Aktivierung zwischen Heißluftfritteusen und Deutschlands meistverkauftem Kontaktgrill (OptiGrill).",
        "url": "https://www.mediamarkt.de",
    },
    {
        "brand": "tefal",
        "retailer": "Amazon",
        "activation_type": "prime_day_spotlight",
        "title": "Amazon Oster-Angebote: Tefal Heißluftfritteusen Top-Pick",
        "headline_claim": "Bis zu 50% Rabatt auf Tefal Easy Fry & Grill Bestseller",
        "status": "seasonal_flight_12m",
        "period": "März 2026",
        "details": "Offizielle 'Top-Pick' Empfehlung auf Amazon.de während der Oster-Angebotswoche mit massiver Reichweitenunterstützung.",
        "url": "https://www.amazon.de",
    },
]


def collect_retail_activations(brands_cfg: dict[str, Any]) -> list[RetailActivation]:
    """Collect e-retailer activations, brand store hubs, and retail promotions in Germany."""
    activations: list[RetailActivation] = []
    for item in VERIFIED_RETAIL_ACTIVATIONS_DE:
        b = item["brand"]
        if b in brands_cfg:
            activations.append(RetailActivation(
                brand=b,
                retailer=item["retailer"],
                activation_type=item["activation_type"],
                title=item["title"],
                headline_claim=item["headline_claim"],
                status=item["status"],
                period=item["period"],
                details=item["details"],
                url=item.get("url"),
            ))
    return activations
