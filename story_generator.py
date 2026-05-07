"""
story_generator.py
Generates Tagalog fruit character stories using the FREE Ollama (local AI)
or falls back to free web-based prompting via requests.

FREE option: Ollama runs a local AI model on your PC (zero API cost).
Install: https://ollama.ai  then run: ollama pull llama3
"""

import requests
import json
import random


def generate_tagalog_story(fruit: str, theme: str) -> dict:
    """
    Generate a Tagalog short story for a fruit character.
    Tries Ollama (local, 100% free) first.
    Falls back to a template story if Ollama is not installed.
    """
    prompt = build_prompt(fruit, theme)

    # Try local Ollama first (free, no internet needed)
    story_text = try_ollama(prompt)

    # Fallback: use template
    if not story_text:
        print("  ⚠️  Ollama not found. Using template story.")
        story_text = get_template_story(fruit, theme)

    # Build title, description, and tags
    title = build_title(fruit, theme)
    description = build_description(fruit, theme)
    tags = build_tags(fruit, theme)

    return {
        "fruit": fruit,
        "theme": theme,
        "title": title,
        "story_text": story_text,
        "description": description,
        "tags": tags,
    }


def build_prompt(fruit: str, theme: str) -> str:
    return f"""
Sumulat ng maikling kuwento sa Tagalog tungkol sa isang prutas na karakter.

Mga detalye:
- Karakter: {fruit}
- Tema: {theme}
- Haba: 5-7 pangungusap lang
- Istilo: dramatic at nakakaaliw, para sa TikTok/YouTube Shorts
- Dapat may simula, gitna, at katapusan
- Gamitin ang mga emosyon para maging engaging

Isulat lang ang kuwento, walang iba.
""".strip()


def try_ollama(prompt: str) -> str:
    """Call local Ollama API (free, runs on your PC)."""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.9, "num_predict": 300}
            },
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        pass  # Ollama not running
    except Exception as e:
        print(f"  Ollama error: {e}")
    return None


def get_template_story(fruit: str, theme: str) -> str:
    """
    Pre-written template stories in Tagalog.
    Used when Ollama is not available.
    """
    templates = {
        "pagmamahal": (
            f"Si {fruit} ay isang prutas na puno ng pag-ibig. "
            f"Araw-araw, pinoprotektahan niya ang kanyang pamilya sa bundok. "
            f"Ngunit isang araw, dumating ang bagyo at sinubukan ang lahat. "
            f"Hindi siya sumusuko — dahil ang pag-ibig niya ay mas malakas pa sa anumang bagyo. "
            f"Sa huli, natuklasan niya na ang tunay na lakas ay galing sa puso."
        ),
        "katapangan": (
            f"Si {fruit} ay takot sa dilim. "
            f"Lagi siyang nakatago sa likod ng ibang mga prutas. "
            f"Ngunit nang kailanganin ang isang bayani, siya lang ang naroroon. "
            f"Lumaban siya kahit nanginginig ang kanyang mga kamay. "
            f"At nang manalo siya, natuklasan niya — ang tapang ay hindi kawalan ng takot, "
            f"kundi ang paglaban kahit may takot ka."
        ),
        "pagkakaibigan": (
            f"Si {fruit} at ang kanyang pinakamabuting kaibigan ay hindi nagkakasundo. "
            f"Nagalit sila sa isa't isa dahil sa isang maliit na bagay. "
            f"Maraming araw ang lumipas nang walang usapan. "
            f"Hanggang sa isang gabi, naalala ni {fruit} ang lahat ng magagandang alaala. "
            f"Lumakad siya sa bahay ng kanyang kaibigan at sinabi: 'Ikaw ang aking puso.'"
        ),
        "selos": (
            f"Si {fruit} ay laging sinasamahan ng lahat. "
            f"Ngunit nang dumating ang bagong prutas sa kanilang grupo, nagbago ang lahat. "
            f"Naramdaman ni {fruit} ang selos na kumakain sa kanyang puso. "
            f"Isang gabi, humarap siya sa salamin at tinanong ang sarili — "
            f"'Bakit ko nararamdaman ito?' At doon niya natuklasan ang sagot."
        ),
        "tagumpay": (
            f"Hindi madali ang buhay ni {fruit}. "
            f"Maraming beses siyang nabigo at nahiya. "
            f"Ngunit bawat pagkakataon, tumayo siya muli. "
            f"Araw-araw, nag-practice siya nang nag-practice. "
            f"At sa araw ng kumpetisyon, nagliwanag ang kanyang ngiti — "
            f"dahil natuklasan niya na ang tagumpay ay para sa mga hindi sumusuko."
        ),
        "pagsasakripisyo": (
            f"Si {fruit} ay may isang pangarap na palayo sa lahat. "
            f"Ngunit ang kanyang pamilya ay nangangailangan ng tulong. "
            f"Pinili niyang isakripisyo ang kanyang sariling kaligayahan. "
            f"Maraming taon ang lumipas. "
            f"At nang makita niya ang ngiti ng kanyang pamilya, "
            f"napagtanto niya — ang tunay na kaligayahan ay ang kaligayahan ng mga mahal mo sa buhay."
        ),
    }
    return templates.get(theme, templates["pagmamahal"])


def build_title(fruit: str, theme: str) -> str:
    title_templates = {
        "pagmamahal": f"Ang Pag-ibig ni {fruit} | Tagalog Fruit Story",
        "katapangan": f"Si {fruit}: Ang Bayani | Tagalog Fruit Story",
        "pagkakaibigan": f"Ang Pagkakaibigan ni {fruit} | Tagalog Fruit Story",
        "selos": f"Si {fruit} at ang Selos | Tagalog Fruit Drama",
        "tagumpay": f"Ang Tagumpay ni {fruit} | Tagalog Fruit Story",
        "pagsasakripisyo": f"Ang Sakripisyo ni {fruit} | Tagalog Fruit Story",
    }
    return title_templates.get(theme, f"Ang Kuwento ni {fruit} | Tagalog Fruit Story")


def build_description(fruit: str, theme: str) -> str:
    return (
        f"Ang dramatikong kuwento ni {fruit} tungkol sa {theme}. "
        f"Panoorin ang kanyang paglalakbay sa buhay! "
        f"\n\n#FruitStory #TagalogStory #AIFruit #FruitDrama #PinoyContent "
        f"#TagalogAI #FruitCharacter #ViralFruit"
    )


def build_tags(fruit: str, theme: str) -> list:
    return [
        "fruit story", "tagalog story", "AI fruit", "fruit drama",
        "pinoy content", "tagalog AI", fruit.lower(), theme,
        "fruit character", "viral fruit", "tiktok fruit", "youtube shorts"
    ]
