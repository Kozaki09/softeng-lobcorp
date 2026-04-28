import random
from flask import Blueprint, jsonify

ads_bp = Blueprint("ads", __name__)

# Shared ad pool — image_url keyed by format for correct sizing
AD_POOL = [
    {
        "id": "ad_001",
        "advertiser": "CloudVault Pro",
        "headline": "Store Everything. Pay Nothing.",
        "body": "10GB free cloud storage. No credit card required.",
        "cta": "Start Free",
        "bg_color": "#0f172a",
        "accent_color": "#38bdf8",
        "image_urls": {
            "skyscraper": "https://picsum.photos/seed/cloudvault/160/200",
            "rectangle":  "https://picsum.photos/seed/cloudvault/300/120",
            "banner":     "https://picsum.photos/seed/cloudvault/728/90",
        },
        "click_url": "#",
    },
    {
        "id": "ad_002",
        "advertiser": "SkillForge",
        "headline": "Learn to Code in 30 Days",
        "body": "Bite-sized lessons trusted by 2M+ developers.",
        "cta": "Try for Free",
        "bg_color": "#1a1a2e",
        "accent_color": "#e94560",
        "image_urls": {
            "skyscraper": "https://picsum.photos/seed/skillforge/160/200",
            "rectangle":  "https://picsum.photos/seed/skillforge/300/120",
            "banner":     "https://picsum.photos/seed/skillforge/728/90",
        },
        "click_url": "#",
    },
    {
        "id": "ad_003",
        "advertiser": "Nomad VPN",
        "headline": "Browse Without Borders",
        "body": "Military-grade encryption. 90+ countries.",
        "cta": "Get Protected",
        "bg_color": "#064e3b",
        "accent_color": "#34d399",
        "image_urls": {
            "skyscraper": "https://picsum.photos/seed/nomadvpn/160/200",
            "rectangle":  "https://picsum.photos/seed/nomadvpn/300/120",
            "banner":     "https://picsum.photos/seed/nomadvpn/728/90",
        },
        "click_url": "#",
    },
    {
        "id": "ad_004",
        "advertiser": "Taskly",
        "headline": "Your Team. In Sync.",
        "body": "Project management that actually makes sense.",
        "cta": "See How",
        "bg_color": "#1e1b4b",
        "accent_color": "#a78bfa",
        "image_urls": {
            "skyscraper": "https://picsum.photos/seed/taskly/160/200",
            "rectangle":  "https://picsum.photos/seed/taskly/300/120",
            "banner":     "https://picsum.photos/seed/taskly/728/90",
        },
        "click_url": "#",
    },
    {
        "id": "ad_005",
        "advertiser": "PulseAnalytics",
        "headline": "Know Your Users",
        "body": "Real-time dashboards. Zero config. Cancel anytime.",
        "cta": "View Demo",
        "bg_color": "#431407",
        "accent_color": "#fb923c",
        "image_urls": {
            "skyscraper": "https://picsum.photos/seed/pulseanalytics/160/200",
            "rectangle":  "https://picsum.photos/seed/pulseanalytics/300/120",
            "banner":     "https://picsum.photos/seed/pulseanalytics/728/90",
        },
        "click_url": "#",
    },
]


def _serialize(ad, fmt):
    """Return ad dict with a flat image_url for the requested format."""
    return {**{k: v for k, v in ad.items() if k != "image_urls"},
            "image_url": ad["image_urls"][fmt]}


@ads_bp.route("/api/ads/banner", methods=["GET"])
def get_banner_ad():
    """Returns a random leaderboard banner ad (728x90)."""
    ad = random.choice(AD_POOL)
    return jsonify({"format": "banner", "width": 728, "height": 90, "ad": _serialize(ad, "banner")})


@ads_bp.route("/api/ads/banner/<ad_id>", methods=["GET"])
def get_specific_banner(ad_id):
    """Returns a specific banner ad by ID."""
    ad = next((a for a in AD_POOL if a["id"] == ad_id), None)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404
    return jsonify({"format": "banner", "width": 728, "height": 90, "ad": _serialize(ad, "banner")})


@ads_bp.route("/api/ads/skyscraper", methods=["GET"])
def get_skyscraper_ad():
    """Returns a random skyscraper ad (160x600)."""
    ad = random.choice(AD_POOL)
    return jsonify({"format": "skyscraper", "width": 160, "height": 600, "ad": _serialize(ad, "skyscraper")})


@ads_bp.route("/api/ads/rectangle", methods=["GET"])
def get_rectangle_ad():
    """Returns a random rectangle ad (300x250)."""
    ad = random.choice(AD_POOL)
    return jsonify({"format": "rectangle", "width": 300, "height": 250, "ad": _serialize(ad, "rectangle")})


@ads_bp.route("/api/ads/skyscraper/<ad_id>", methods=["GET"])
def get_specific_skyscraper(ad_id):
    """Returns a specific skyscraper ad by ID."""
    ad = next((a for a in AD_POOL if a["id"] == ad_id), None)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404
    return jsonify({"format": "skyscraper", "width": 160, "height": 600, "ad": _serialize(ad, "skyscraper")})


@ads_bp.route("/api/ads/rectangle/<ad_id>", methods=["GET"])
def get_specific_rectangle(ad_id):
    """Returns a specific rectangle ad by ID."""
    ad = next((a for a in AD_POOL if a["id"] == ad_id), None)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404
    return jsonify({"format": "rectangle", "width": 300, "height": 250, "ad": _serialize(ad, "rectangle")})