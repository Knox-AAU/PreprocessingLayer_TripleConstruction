import json

import nltk
import random

# Check if punkt is already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    # Download punkt if not found
    print("Downloading punkt...")
    nltk.download('punkt')
    print("Download complete.")


class EntityGenerator:
    def __init__(self):
        self.classifications = {}

    def add_classification(self, classification, templates):
        self.classifications[classification] = templates

    def generate_sentence(self, classification):
        if classification not in self.classifications:
            print(f"Error: Classification '{classification}' not found.")
            return None

        templates = self.classifications[classification]
        template = random.choice(templates)

        entity = self.generate_entity()
        sentence = template.replace('{entity}', entity)
        return sentence, entity, classification

    def generate_entity(self):
        # Generate a completely random entity mention with varying word counts
        word_count = random.randint(1, 3)  # Adjust the range as needed
        words = [self.generate_random_word() for _ in range(word_count)]
        entity = ' '.join(words)
        return entity.capitalize()

    def generate_random_word(self):
        # Generate a random word
        word_length = random.randint(3, 8)  # Adjust the range as needed
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(word_length))

# Example Usage:
entity_generator = EntityGenerator()

# Define more comprehensive templates for each classification
entity_generator.add_classification('Person', [
    '{entity} explores the wonders of the natural world',
    'In the realm of creativity, {entity} shapes unique expressions',
    'Philosophy finds a companion in the thoughts of {entity}',
    '{entity} captivates with a blend of humor and insight',
    'The stage comes alive with the presence of {entity}',
    '{entity} narrates stories with a distinctive voice',
    'Behind the scenes, {entity} orchestrates visual magic',
    'Musical notes dance to the rhythm of {entity}',
    '{entity} delves into the mysteries of the universe',
    'Athletic prowess defines {entity} on the field of play',
    'Arrows find their mark with precision in the hands of {entity}',
    'The court is a stage for {entity} in the game of sport',
    'Bats and balls align in harmony with {entity}',
    '{entity} channels strength into physical discipline',
    'The ring is a canvas for {entity} in the world of combat',
    'Adventures on water define {entity} in aquatic pursuits',
    'Strategic brilliance defines {entity} in the world of games',
    '{entity} excels on the cricket pitch with skill',
    'Cycling routes become a journey for {entity}',
    'Precision and skill meet in the world of darts with {entity}',
    'Fencing becomes an art form in the hands of {entity}',
    '{entity} explores the fast-paced world of Gaelic games',
    'Greens transform into a playground for {entity} in golf',
    'Gridiron battles witness the prowess of {entity}',
    '{entity} tackles opponents with finesse in sports',
    'Fields resonate with the moves of {entity}',
    '{entity} brings elegance to gymnastics routines',
    'Handball courts witness the agility of {entity}',
    'Diving into new heights, {entity} masters the art of performance',
    '{entity} rides with grace in the world of equestrian pursuits',
    'Jockeying for position, {entity} conquers racing tracks',
    'Lacrosse fields witness the finesse of {entity}',
    'Martial arts mastery defines {entity}',
    '{entity} races to victory in motorsports',
    'Motorcycles roar to life under the control of {entity}',
    'Speedway tracks witness the skill of {entity}',
    'The race track is a canvas for {entity} in motorsports',
    '{entity} maneuvers through the world of motorsports',
    'Rallying to success, {entity} conquers diverse terrains',
    '{entity} competes at the highest level in sports',
    'The net becomes a playground for {entity}',
    '{entity} bluffs their way to success in games',
    'Rowing becomes a rhythm for {entity}',
    '{entity} shows strength on the rugby field',
    'Sailing through challenges, {entity} conquers the seas',
    'Precision defines {entity} in the world of competitions',
    'Games tables witness the skill of {entity}',
    '{entity} dribbles to success in the game of sport',
    'Courts echo with the skill of {entity}',
    'Waves become a playground for {entity} in surfing',
    '{entity} glides through water with mastery',
    'Tables resonate with the skill of {entity}',
    'Team dynamics define success for {entity} in collective efforts',
    '{entity} serves with precision in the game of tennis',
    'Spikes and blocks define success for {entity}',
    'Sand becomes a canvas for {entity}',
    'Water arenas echo with the strength of {entity}',
    '{entity} conquers icy landscapes in winter pursuits',
    'Trails become a journey for {entity}',
    'Sliding through icy paths, {entity} conquers winter sports',
    'Ice skates glide gracefully under the control of {entity}',
    '{entity} leaps into the world of ski jumping',
    'Ski slopes become a playground for {entity}',
    'Speed becomes an art form for {entity} in skating',
    'The wrestling ring witnesses the strength of {entity}',
    '{entity} embraces the traditions of wrestling',
    'Elegance defines {entity} in various pursuits',
    '{entity} navigates the complexities of business',
    'Culinary creations define the expertise of {entity}',
    '{entity} guides souls on their personal journeys',
    'Cardinals gather to discuss matters with {entity}',
    'Theology becomes a pursuit for {entity}',
    '{entity} imparts wisdom in the realms of law',
    'Linguistic expertise defines {entity}',
    '{entity} stands as a symbol of individuality',
    'Military strategy is shaped by {entity}',
    '{entity} graces various arenas with elegance',
    'The royal court acknowledges the presence of {entity}',
    '{entity} takes charge of political landscapes',
    'Diplomatic missions find success with {entity}',
    'Government leadership defines {entity}',
    '{entity} presides over parliamentary affairs',
    '{entity} takes the oath as a representative',
    'Duties define the days of {entity}',
    '{entity} represents the voice of the people',
    'Debates echo with the opinions of {entity}',
    '{entity} supports leadership in various capacities',
    'Responsibilities rest on {entity}',
    '{entity} shares the stage as a presenter',
    'Airwaves resonate with the voice of {entity}',
    'Screens light up with the presence of {entity}',
    '{entity} brings creative visions to various screens',
    'Psychological insights define the work of {entity}',
    'Referees ensure fair play under the watchful eye of {entity}',
    '{entity} delves into the mysteries of the mind',
    'Spiritual teachings find resonance with {entity}',
    'Leadership defines the role of {entity}',
    'Rulers shape the destiny of nations, as did {entity}',
    'The crown symbolizes the reign of {entity}',
    '{entity} studies the annals of history',
    'Compositions resonate with the genius of {entity}',
    '{entity} weaves stories on the stage',
    'Verses echo with the poetic prowess of {entity}',
    'Scripts come to life under the pen of {entity}',
    'Lyrics come alive with the creativity of {entity}',
    '{entity} shares insights through the lens of YouTube'
])

entity_generator.add_classification('Place', [
    '{entity} is a beautiful city',
    'People love visiting {entity}',
    '{entity} is famous for its historic landmarks',
    'The skyline of {entity} is breathtaking',
    '{entity} is surrounded by mountains'
    "{entity} is known for its scenic beauty and vibrant culture",
    "In the heart of nature, {entity} unfolds its wonders",
    "{entity} embraces a diverse mix of landscapes and traditions",
    "Exploring {entity} reveals a tapestry of natural wonders",
    "Cultural richness thrives in the heart of {entity}",
    "Journey through {entity} to discover its hidden gems",
    "{entity} captivates with a harmonious blend of nature and heritage",
    "In {entity}, diverse landscapes coexist with historical charm",
    "{entity} stands as a testament to natural diversity and human history",
    "Discover the enchanting allure of {entity} and its unique character",
    "{entity} is a haven where nature and culture converge",
    "Cradled in nature, {entity} is a mosaic of beauty",
    "The spirit of {entity} lies in its varied landscapes and stories",
    "{entity} unfolds its secrets through a blend of nature and culture",
    "Nature's masterpiece, {entity} is a sanctuary of tranquility",
    "{entity} harmonizes natural wonders with cultural treasures",
    "Explore the hidden corners of {entity} to uncover its splendors",
    "{entity} invites exploration with its diverse geographical features",
    "Cultural heritage and natural beauty intertwine in {entity}",
    "{entity} is a canvas painted with the hues of diversity",
    "Traverse through {entity} and be mesmerized by its landscapes",
    "In the embrace of nature, {entity} exudes timeless charm",
    "{entity} is a living canvas, portraying nature's wonders",
    "From mountains to valleys, {entity} weaves a picturesque tale",
    "{entity} invites wanderers to immerse in its cultural mosaic",
    "Nature's wonders unfold in the breathtaking landscapes of {entity}",
    "{entity} preserves the echoes of history within its scenic embrace",
    "Diverse ecosystems thrive in the heart of {entity}",
    "Discover the serenity and beauty of {entity}",
    "{entity} unfolds a story written in the language of landscapes"
])

entity_generator.add_classification('Organisation', [
    "The team at {entity} fosters innovation and collaboration",
    "As a leading force, {entity} stands out in the realm of progress",
    "{entity} serves as a hub of diverse talents and expertise",
    "The initiatives led by {entity} reveal a commitment to excellence",
    "Collaboration thrives within the organizational walls of {entity}",
    "Journeying through the mission of {entity} unveils impactful endeavors",
    "Guided by a vision of positive change, {entity} takes the lead",
    "Within {entity}, diverse skills converge for common goals",
    "{entity} stands as a testament to collective achievement and collaboration",
    "Discover the impact and shared values of {entity}",
    "{entity} operates dynamically, shaping the future with purpose",
    "Rooted in purpose, {entity} makes a meaningful impact on society",
    "The spirit of {entity} is embodied in its commitment to progress",
    "{entity} unfolds its significant contributions to society",
    "As a beacon of excellence, {entity} drives positive change",
    "{entity} harmonizes diverse talents towards organizational success",
    "Explore the legacy and influence of {entity} in various endeavors",
    "{entity} invites individuals to actively contribute to its mission",
    "Collaborative efforts define the essence of {entity}'s work",
    "{entity} is a canvas painted with the vibrant colors of progress",
    "Traverse through the organizational achievements of {entity}",
    "In the world of impactful initiatives, {entity} exudes leadership",
    "{entity} is a living embodiment of positive organizational change",
    "From visionary ideas to tangible reality, {entity} weaves a success story",
    "{entity} invites contributors to immerse in its impactful mission",
    "In the spirit of organizational progress, {entity} stands tall",
    "{entity} preserves a legacy of meaningful organizational contributions",
    "Diverse talents find a home within the organizational mission of {entity}",
    "Discover the dynamism and organizational impact of {entity}",
    "{entity} unfolds a story of dedication and organizational achievement"
])

# Generate and print sentences with full names
# Generate JSON object similar to the provided example
generated_data = []
for _ in range(5000):  # Adjust the number of sentences as needed
    classification = random.choice(list(entity_generator.classifications.keys()))
    sentence, entity, _ = entity_generator.generate_sentence(classification)
    entity_mention = {
        "name": entity,
        "type": "Entity",
        "label": classification,
        "startIndex": None,
        "endIndex": None,
        "iri": None,
        "classification": classification
    }
    sentence_data = {
        "sentence": sentence,
        "sentenceStartIndex": 0,
        "sentenceEndIndex": len(sentence),
        "entityMentions": [entity_mention]
    }
    generated_data.append(sentence_data)

# Create the final JSON object
final_json_object = [{
    "language": "en",
    "metadataId": "790261e8-b8ec-4801-9cbd-00263bcc666d",
    "sentences": generated_data
}]

# Specify the file path
file_path = '../generate_dataset/generated_data.json'

# Write the JSON object to a file
with open(file_path, 'w') as json_file:
    json.dump(final_json_object, json_file, indent=2)

print(f"JSON object written to {file_path}")