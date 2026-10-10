import re

HAPPY = re.compile(r'\b(love|happy|joy|joyful|joyous|excited|exciting|thrilled|amazing|fantastic|wonderful|excellent|delighted|grateful|blessed|bliss|blissful|ecstatic|proud|winning|won|celebrating|celebrate|celebration|success|successful|smiling|smile|grinning|laughing|laughter|beautiful|perfect|fulfilled|elated|cheerful|cheered|optimistic|relieved|overjoyed|pleased|content|adorable|uplifting|incredible|best|awesome)\b|cloud nine|dream come true|tears of joy|couldn.t be happier|on top of the world|made my day|looking forward|all my hard work paid off', re.I)

SAD = re.compile(r'\b(sad|sadness|lost|heartbroken|heartbreak|worst|terrible|awful|horrible|hate|disappointed|disappointing|lonely|alone|abandoned|depressed|depression|hopeless|hopelessness|hurt|pain|painful|grief|grieving|crying|cried|tears|devastated|miserable|miserably|unhappy|rejected|rejection|regret|regretting|betrayal|betrayed|failure|failed|defeated|anxiety|anxious|traumatized|sorrow|sorrowful|angry|frustrated|frustrating|dread|despair|ruined|layoffs|empty|disaster|disastrous|unbearable|upset|crushed|broken|gloomy|downcast|discouraged|disheartened)\b|passed away|falling apart|ended badly|nobody showed|no one cares|bad news|worse|nothing goes right', re.I)

def classify(text):
    positive = len(HAPPY.findall(text))
    negative = len(SAD.findall(text))
    positive += len(re.findall(r'\b(happiest|happiness|excitement|fortunate|energized|spectacular)\b|exactly what I was hoping for|exceeded all my expectations', text, re.I))
    negative += len(re.findall(r'\b(worried|burdened)\b|endless problems', text, re.I))
    if re.search(r'\b(not|never)\s+(?:very\s+)?(?:happy|good|excited|pleased)', text, re.I):
        negative += 2
    if re.search(r'\b(not|never)\s+(?:very\s+)?(?:sad|unhappy|disappointed)', text, re.I):
        positive += 2
    if 'tears of joy' in text.lower():
        positive += 2
    return 'happy' if positive > negative else 'sad' if negative > positive else 'neutral'
