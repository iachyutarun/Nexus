import os
import re
import webbrowser
from datetime import datetime
from nexus.commands.calculator import safe_calculate
from nexus.commands.notes import notes_list, notes_add, notes_search, notes_delete
from nexus.commands.system import get_system_status
from nexus.commands.files import list_files, search_files
from nexus.commands.history import get_history, clear_history, add_history
from nexus.commands.about import get_about, get_version

SITES = {
    'google': 'https://www.google.com',
    'youtube': 'https://www.youtube.com',
    'github': 'https://github.com',
    'wikipedia': 'https://www.wikipedia.org',
    'reddit': 'https://www.reddit.com',
    'twitter': 'https://twitter.com',
    'x': 'https://x.com',
    'bing': 'https://www.bing.com',
    'amazon': 'https://www.amazon.com',
    'netflix': 'https://www.netflix.com',
    'stackoverflow': 'https://stackoverflow.com',
    'quora': 'https://www.quora.com',
    'medium': 'https://medium.com',
}

GREETINGS = ['hi', 'hello', 'hey', 'howdy', 'greetings', 'good morning', 'good afternoon', 'good evening']
GREETING_RESPONSES = [
    "Hello! I'm NEXUS, your portable AI terminal. How can I assist you today?",
    "Greetings! I'm ready to help with calculations, notes, system info, and general knowledge.",
    "Hey there! What would you like to explore or accomplish?",
    "Hi! I'm online and ready. Type 'help' to see what I can do.",
]

class RuleBasedEngine:
    def __init__(self, output_callback=None, confirm_callback=None, ai_engine=None):
        self.output_callback = output_callback or (lambda x: x)
        self.confirm_callback = confirm_callback or (lambda msg: True)
        self.ai_engine = ai_engine

    def process(self, text, username=None):
        text = text.strip()
        if not text:
            return ""
        lower = text.lower()

        if lower in ('help', 'commands'):
            return self._help()
        if lower in ('clear', 'cls'):
            return '__CLEAR__'
        if lower in ('status', 'system status', 'system', 'show system status'):
            return self._status()
        if lower.startswith('calculate ') or lower.startswith('calc ') or lower.startswith('math '):
            expr = text.split(' ', 1)[1]
            result, err = safe_calculate(expr)
            if err:
                return f"Calculation error: {err}"
            return f"Result: {result}"
        if lower in ('notes', 'show notes', 'list notes'):
            return notes_list(username)
        if lower.startswith('notes add '):
            title = text.split(' ', 2)[2] if len(text.split(' ', 2)) > 2 else ''
            return notes_add(title, '', username)
        if lower.startswith('notes search '):
            query = text.split(' ', 2)[2]
            return notes_search(query, username)
        if lower.startswith('notes delete '):
            note_id = text.split(' ', 2)[2]
            return notes_delete(note_id, username)
        if lower in ('files', 'list files', 'dir'):
            return list_files()
        if lower.startswith('files '):
            path = text.split(' ', 1)[1]
            return list_files(path)
        if lower.startswith('search '):
            query = text.split(' ', 1)[1]
            return search_files(query)
        if lower in ('history', 'show history'):
            return get_history(username)
        if lower == 'history clear':
            if self.confirm_callback("Clear command history? (yes/no):"):
                return clear_history(username)
            return "Cancelled."
        if lower in ('about', 'info'):
            return get_about()
        if lower in ('version', 'ver'):
            return get_version()
        if lower in ('logout', 'exit', 'quit'):
            return '__LOGOUT__'
        if lower == 'demo':
            return '__DEMO__'
        if lower in ('model', 'model status', 'ai status'):
            return self._model_status()
        if lower.startswith('model on '):
            path = text.split(' ', 2)[2]
            return self._model_on(path)
        if lower == 'model off':
            return self._model_off()
        if lower in ('time', 'date', 'datetime', 'clock'):
            return self._datetime()
        if lower in ('who are you', 'what are you', 'introduce yourself'):
            return "I am NEXUS, a portable AI terminal running locally from your USB drive. I can answer questions, perform calculations, manage notes, check system status, and help you navigate the web."
        browser_result = self._try_browser(text)
        if browser_result is not None:
            return browser_result
        greeting_result = self._try_greeting(text)
        if greeting_result is not None:
            return greeting_result
        return self._general_knowledge(text)

    def _help(self):
        return """AVAILABLE COMMANDS:
  help              - Show this help
  clear / cls       - Clear terminal
  status            - System status
  calculate <expr>  - Safe calculator
  notes             - List notes
  notes add <title> - Create note
  notes search <q>  - Search notes
  notes delete <id> - Delete note
  files             - List files in USB/data
  files <path>      - List specific path
  search <query>    - Search files
  history           - Command history
  history clear     - Clear history
  about             - About NEXUS
  version           - Version info
  logout / exit     - Logout
  demo              - Exhibition mode
  model status      - Show local model status
  model off         - Disable local model
  time / date       - Show current date and time
  open <site/url>   - Open website in default browser

Sites: google, youtube, github, wikipedia, reddit, twitter, bing, amazon, netflix, stackoverflow, quora, medium

You can also ask natural questions like:
  "what is Python?"
  "explain gravity"
  "who is Gandhi?"
  "tell me about space"
  "how does photosynthesis work?"
  "calculate 25 * 17"
  "open youtube"

NOTE: If a GGUF model is placed in models/ and ctransformers
is installed on the host, NEXUS auto-enables it on startup."""

    def _status(self):
        s = get_system_status()
        return f"""SYSTEM STATUS
CPU:    {s['cpu']}
RAM:    {s['ram']}
DISK:   {s['disk']}
OS:     {s['os']}
HOST:   {s['hostname']}
UPTIME: {s['uptime']}
NET:    {s['network']}"""

    def _datetime(self):
        now = datetime.now()
        return now.strftime("Current date and time: %Y-%m-%d %H:%M:%S")

    def _try_greeting(self, text):
        lower = text.lower().strip()
        if lower in GREETINGS:
            import random
            return random.choice(GREETING_RESPONSES)
        return None

    def _general_knowledge(self, text):
        lower = text.lower()
        prefixes = ['what is', 'what are', 'explain', 'who is', 'who was', 'tell me about', 'define', 'describe', 'how does', 'how do', 'why is', 'why are', 'when was', 'where is', 'where are']
        if any(lower.startswith(p) for p in prefixes):
            topic = text
            for p in prefixes:
                if lower.startswith(p):
                    topic = text[len(p):].strip()
                    break
            return self._knowledge_response(topic)
        if any(k in lower for k in ['how much ram', 'ram usage', 'memory usage', 'memory']):
            return self._status()
        if any(k in lower for k in ['cpu usage', 'how much cpu', 'processor']):
            s = get_system_status()
            return f"CPU usage: {s['cpu']}"
        if any(k in lower for k in ['time', 'date', 'clock']):
            return self._datetime()
        browser_result = self._try_browser(text)
        if browser_result is not None:
            return browser_result
        return (f"I understood your request, but I can only help with built-in commands and general "
                f"knowledge. Try 'help' to see what I can do.\n"
                f"Your query: {text}")

    def _knowledge_response(self, topic):
        topic = topic.strip().rstrip('?').strip()
        lower = topic.lower()
        mapping = {
            'python': "Python is a high-level, interpreted programming language created by Guido van Rossum and first released in 1991.",
            'gravity': "Gravity is a fundamental interaction that causes mutual attraction between all things with mass or energy.",
            'photosynthesis': "Photosynthesis is the process used by plants, algae, and some bacteria to convert light energy into chemical energy stored in glucose.",
            'nexus': "NEXUS is a portable AI terminal application designed to run from a USB drive.",
            'artificial intelligence': "Artificial Intelligence is the simulation of human intelligence processes by computer systems, including learning, reasoning, and self-correction.",
            'internet': "The Internet is a global network of interconnected computers that communicate using standardized protocols.",
            'computer': "A computer is an electronic device that processes data according to instructions called programs.",
            'united states': "The United States of America is a country primarily located in North America.",
            'mahatma gandhi': "Mahatma Gandhi, born Mohandas Karamchand Gandhi, was the leader of India's non-violent independence movement against British rule. He is known for the principles of truth and non-violence.",
            'mohandas gandhi': "Mahatma Gandhi, born Mohandas Karamchand Gandhi, was the leader of India's non-violent independence movement against British rule. He is known for the principles of truth and non-violence.",
            'subhash chandra bose': "Subhash Chandra Bose was an Indian nationalist whose defiance of British authority made him a hero in India.",
            'solar system': "The Solar System consists of the Sun and the objects bound to it by gravity, including eight planets, dwarf planets, moons, and asteroids.",
            'machine learning': "Machine Learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.",
            'climate change': "Climate change refers to long-term shifts in global temperatures and weather patterns. Human activities are the main driver of recent climate change.",
            'milky way': "The Milky Way is the galaxy that contains our Solar System. It is a barred spiral galaxy with an estimated 100-400 billion stars.",
            'black hole': "A black hole is a region of spacetime where gravity is so strong that nothing, including light, can escape from it.",
            'usa': "The United States of America is a country primarily located in North America.",
            'india': "India is a country in South Asia, known for its diverse culture, history, and technology industry.",
            'london': "London is the capital and largest city of England and the United Kingdom.",
            'paris': "Paris is the capital and most populous city of France.",
            'tokyo': "Tokyo is the capital and most populous city of Japan.",
            'einstein': "Albert Einstein was a theoretical physicist known for developing the theory of relativity.",
            'newton': "Isaac Newton was an English mathematician, physicist, and astronomer known for his laws of motion and universal gravitation.",
            'tesla': "Nikola Tesla was a Serbian-American inventor known for his contributions to the design of the modern alternating current electricity supply system.",
            'moon': "The Moon is Earth's only natural satellite and the fifth largest moon in the Solar System.",
            'sun': "The Sun is the star at the center of the Solar System.",
            'earth': "Earth is the third planet from the Sun and the only astronomical object known to harbor life.",
            'water': "Water is a transparent, tasteless, odorless, and nearly colorless chemical substance that is the main constituent of Earth's hydrosphere.",
            'fire': "Fire is a chemical reaction that releases heat and light, typically involving the rapid oxidation of a material.",
            'gandhiji': "Mahatma Gandhi, born Mohandas Karamchand Gandhi, was the leader of India's non-violent independence movement against British rule. He is known for the principles of truth and non-violence.",
            'gandhi': "Mahatma Gandhi, born Mohandas Karamchand Gandhi, was the leader of India's non-violent independence movement against British rule. He is known for the principles of truth and non-violence.",
            'nehru': "Jawaharlal Nehru was the first Prime Minister of India and a central figure in Indian politics for decades.",
            'ambedkar': "Dr. B.R. Ambedkar was the chief architect of the Indian Constitution and a champion of social justice.",
            'sardar patel': "Sardar Vallabhbhai Patel was an Indian statesman known as the Iron Man of India for integrating the princely states.",
            'space': "Space is the vast three-dimensional expanse in which objects and events occur. It includes the solar system, stars, galaxies, and the universe.",
            'universe': "The universe is all of space and time and their contents, including planets, stars, galaxies, and all forms of matter and energy.",
            'mars': "Mars is the fourth planet from the Sun, often called the Red Planet due to iron oxide on its surface.",
            'jupiter': "Jupiter is the largest planet in our solar system, known for its Great Red Spot and many moons.",
            'saturn': "Saturn is the sixth planet from the Sun, famous for its prominent ring system made of ice and rock.",
            'venus': "Venus is the second planet from the Sun, known as the hottest planet in our solar system.",
            'mercury': "Mercury is the smallest planet in our solar system and the closest to the Sun.",
            'pluto': "Pluto is a dwarf planet in the Kuiper Belt, reclassified from planet status in 2006.",
            'galaxy': "A galaxy is a huge collection of gas, dust, and billions of stars and their solar systems, all held together by gravity.",
            'light': "Light is electromagnetic radiation that can be detected by the human eye. It travels at approximately 299,792 kilometers per second in a vacuum.",
            'energy': "Energy is the capacity to do work. It exists in various forms including kinetic, potential, thermal, chemical, and nuclear energy.",
            'electricity': "Electricity is the set of physical phenomena associated with the presence and motion of electric charge.",
            'magnetism': "Magnetism is a physical phenomenon produced by the motion of electric charge, resulting in attractive and repulsive forces between objects.",
            'atom': "An atom is the smallest unit of ordinary matter that forms a chemical element. It consists of a nucleus and electrons.",
            'dna': "DNA, or deoxyribonucleic acid, is the molecule that carries genetic instructions for the development, functioning, growth, and reproduction of all known organisms.",
            'cell': "The cell is the basic structural, functional, and biological unit of all living organisms.",
            'brain': "The brain is the central organ of the human nervous system. It controls most activities of the body and is the seat of intelligence and consciousness.",
            'heart': "The heart is a muscular organ that pumps blood through the blood vessels of the circulatory system.",
            'blood': "Blood is a body fluid that circulates throughout the human body delivering nutrients and oxygen to cells and removing metabolic waste.",
            'oxygen': "Oxygen is a chemical element essential for most forms of life on Earth. It is used in cellular respiration.",
            'carbon': "Carbon is a chemical element with symbol C. It is the basis of all known life on Earth and forms many compounds.",
            'hydrogen': "Hydrogen is the lightest and most abundant chemical element in the universe, making up about 75% of all normal matter.",
            'helium': "Helium is the second lightest and second most abundant element in the observable universe.",
            'gold': "Gold is a chemical element with symbol Au. It is a bright, slightly reddish yellow, dense, soft, and malleable metal.",
            'silver': "Silver is a chemical element with symbol Ag. It is a soft, white, lustrous transition metal with the highest electrical conductivity of any element.",
            'iron': "Iron is a chemical element with symbol Fe. It is the most common element on Earth by mass, forming much of Earth's outer and inner core.",
            'diamond': "Diamond is a solid form of carbon with a diamond cubic crystal structure. It is the hardest known natural material.",
            'oil': "Oil is a non-renewable fossil fuel formed from ancient organic matter. It is used for energy, transportation, and manufacturing.",
            'coal': "Coal is a combustible black or brownish-black sedimentary rock formed from ancient plant matter. It is used as a fuel source.",
            'wind': "Wind is the natural movement of air relative to the surface of the Earth. It is caused by differences in atmospheric pressure.",
            'rain': "Rain is liquid water that falls from clouds in the form of droplets. It is part of the water cycle.",
            'cloud': "A cloud is a visible mass of condensed water droplets or ice crystals suspended in the atmosphere.",
            'snow': "Snow is a type of precipitation in the form of ice crystals. It forms when water vapor freezes directly into ice.",
            'ocean': "The ocean is a body of saline water that composes much of a planet's hydrosphere. On Earth, the ocean covers about 71% of the surface.",
            'river': "A river is a natural flowing watercourse, usually freshwater, flowing towards an ocean, sea, lake, or another river.",
            'mountain': "A mountain is a large landform that rises prominently above its surroundings, typically having steep slopes and a summit.",
            'forest': "A forest is a large area dominated by trees. Forests are essential for life on Earth as they provide oxygen, habitat, and resources.",
            'animal': "Animals are multicellular, eukaryotic organisms of the kingdom Animalia. They consume organic material, breathe oxygen, and can move voluntarily.",
            'human': "Humans, or Homo sapiens, are the most abundant and widespread species of primate on Earth, characterized by bipedalism and complex brains.",
            'robot': "A robot is a machine capable of carrying out tasks automatically. Robots can be guided by an external control device or controlled internally.",
            'ai': "Artificial Intelligence is the simulation of human intelligence processes by computer systems, including learning, reasoning, and self-correction.",
            'blockchain': "Blockchain is a distributed ledger technology that records transactions across many computers so that the record cannot be altered retroactively.",
            'bitcoin': "Bitcoin is a decentralized digital currency without a central bank or single administrator. It was created in 2009 by an unknown person using the name Satoshi Nakamoto.",
            'cryptocurrency': "Cryptocurrency is a digital or virtual currency that uses cryptography for security and operates independently of a central bank.",
            'vaccine': "A vaccine is a biological preparation that provides active acquired immunity to a particular infectious or deadly disease.",
            'antibiotic': "An antibiotic is a type of antimicrobial substance active against bacteria. It is the most important type of antibacterial agent.",
            'virus': "A virus is a small infectious agent that can only replicate inside the living cells of an organism. Viruses can infect all types of life forms.",
            'bacteria': "Bacteria are single-celled microorganisms that live in diverse environments. Some bacteria cause disease while others are beneficial.",
            'fungus': "Fungi are a kingdom of organisms that include mushrooms, yeasts, and molds. They absorb nutrients from organic matter.",
            'pollution': "Pollution is the introduction of harmful materials or products into the environment. It can cause adverse effects on living organisms and ecosystems.",
            'recycling': "Recycling is the process of converting waste materials into new materials and objects. It helps reduce waste, conserve resources, and protect the environment.",
            'democracy': "Democracy is a system of government in which power is vested in the people, who rule either directly or through freely elected representatives.",
            'economy': "An economy is the large set of inter-related production, consumption, and exchange activities that aid in determining how scarce resources are allocated.",
            'math': "Mathematics is the abstract science of number, quantity, and space. It includes arithmetic, algebra, geometry, calculus, and statistics.",
            'algebra': "Algebra is a branch of mathematics dealing with symbols and the rules for manipulating those symbols. It is a unifying thread of almost all of mathematics.",
            'geometry': "Geometry is the branch of mathematics concerned with the properties and relations of points, lines, surfaces, and solids.",
            'physics': "Physics is the natural science that studies matter, its fundamental constituents, its motion and behavior through space and time, and related entities.",
            'chemistry': "Chemistry is the scientific study of the properties and behavior of matter. It is a physical science that studies the composition, structure, and properties of matter.",
            'biology': "Biology is the natural science that studies life and living organisms, including their physical structure, chemical processes, molecular interactions, and evolution.",
            'history': "History is the study of the past, particularly how it relates to humans. It includes the study of events, people, cultures, and societies over time.",
            'geography': "Geography is the study of places and the relationships between people and their environments. It explores both the physical properties of Earth's surface and the human societies spread across it.",
            'literature': "Literature is any body of written work. More broadly, literature refers to any collection of written or oral compositions that are considered artistic or intellectual.",
            'music': "Music is the art of arranging sounds in time through the elements of melody, harmony, rhythm, and timbre.",
            'art': "Art is a diverse range of human activity involving creative imagination to express technical proficiency, beauty, emotional power, or conceptual ideas.",
            'philosophy': "Philosophy is the study of fundamental questions about existence, knowledge, values, reason, mind, and language.",
            'psychology': "Psychology is the scientific study of mind and behavior. It includes all aspects of conscious and unconscious experiences and thoughts.",
            'sociology': "Sociology is the study of society, social institutions, and social relationships. It examines how people interact within groups and societies.",
            'engineering': "Engineering is the use of scientific principles to design and build machines, structures, and other items. It includes many fields such as civil, mechanical, electrical, and software engineering.",
            'medicine': "Medicine is the science and practice of establishing a diagnosis, providing prognosis, preventing disease, and treating disease or injury in humans.",
            'law': "Law is a system of rules created and enforced through social or governmental institutions to regulate behavior.",
            'education': "Education is the process of facilitating learning, or the acquisition of knowledge, skills, values, morals, beliefs, habits, and personal development.",
        }
        for key, answer in mapping.items():
            pattern = r'\b' + re.escape(key) + r'\b'
            if re.search(pattern, lower):
                return answer
        return (f"I don't have specific information about '{topic}' in my local knowledge base. "
                f"I can help with commands, calculations, notes, system status, and opening websites.")

    def _model_status(self):
        if self.ai_engine:
            return self.ai_engine.get_model_status()
        return "Model management not available."

    def _model_on(self, path):
        if not self.ai_engine:
            return "Model management not available."
        if not path:
            return "Usage: model on <path_to_model.gguf>"
        if not os.path.exists(path):
            return f"Model file not found: {path}"
        name = self.ai_engine.enable_local_model(path)
        return f"Local model enabled: {name}"

    def _model_off(self):
        if not self.ai_engine:
            return "Model management not available."
        name = self.ai_engine.disable_local_model()
        return f"Switched to: {name}"

    def _try_browser(self, text):
        lower = text.lower()
        if lower.startswith('open ') or lower.startswith('browse '):
            target = text.split(' ', 1)[1].strip()
            return self._open_url(target)
        for name, url in SITES.items():
            if lower.startswith(f'open {name}') or lower.startswith(f'browse {name}'):
                return self._open_url(url)
        return None

    def _open_url(self, target):
        if not target:
            return "Usage: open <site_or_url>"
        if target.startswith('http://') or target.startswith('https://'):
            url = target
        else:
            url = SITES.get(target.lower())
            if not url:
                url = f'https://www.google.com/search?q={target}'
        try:
            webbrowser.open(url)
            return f"Opened: {url}"
        except Exception as e:
            return f"Failed to open browser: {e}"
