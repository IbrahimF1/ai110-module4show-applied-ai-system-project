# 🎵 Music Recommender Simulation

## Project Summary

This project implements a music recommender system that suggests songs based on user preferences. The system uses a mathematical scoring approach that rewards songs for their closeness to user targets. It evaluates seven song features including genre, mood, energy, tempo, valence, danceability, and acousticness. The system calculates similarity scores using a Gaussian function for numerical features and binary matching for categorical features. It then combines these scores using weighted percentages to produce a final recommendation score. The system includes ten predefined user profiles and provides detailed explanations for each recommendation.

---

## How The System Works

Each Song in the system uses seven features: genre, mood, energy, tempo, valence, danceability, and acousticness. The UserProfile stores the user's favorite genre, favorite mood, target energy level, and acoustic preference. The Recommender computes a score for each song by comparing song features to user preferences. It uses binary matching for genre and mood, giving full points for exact matches. For numerical features, it uses a Gaussian similarity function that rewards closeness to target values. The system combines individual feature scores using weighted percentages: genre (25%), mood (15%), energy (20%), tempo (10%), valence (10%), danceability (10%), and acousticness (10%). It then sorts all songs by their final score and returns the top k recommendations.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

I tested the system with seven standard user profiles representing different musical tastes. The system performed well for profiles with consistent preferences like chill lofi lovers and energetic pop fans. I then tested three edge case profiles with contradictory preferences. These tests revealed that the system prioritizes categorical features over numerical ones. For example, a rock song with energy 0.91 scored highly for a profile requesting energy 0.15 because it matched the rock genre and intense mood. I also experimented with different sigma values for the Gaussian function to adjust strictness. Smaller sigma values made the system more selective, while larger values made it more forgiving.

---

## Limitations and Risks

The system only works on a small catalog of 18 songs. It does not understand lyrics, language, or cultural context. The system over-prioritizes categorical features, allowing songs to achieve high scores even when numerical preferences contradict the user's targets. It can be tricked by profiles with impossible combinations like high-energy acoustic music. The system lacks representation for many genres and cultural styles. It treats each feature independently without validating whether preference combinations make realistic sense. The Gaussian similarity function is relatively forgiving, reducing sensitivity to contradictory user preferences.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

I learned that recommenders turn complex user preferences into simple numerical scores through mathematical functions. The system converts categorical and numerical features into comparable scores, then combines them using weighted percentages. This process reveals how bias can emerge when certain features receive disproportionate weight. In this system, categorical features dominate scoring, allowing songs to achieve high recommendations even when numerical preferences contradict user targets. This bias could unfairly favor users whose preferences align with popular genres or moods while penalizing those with unusual or contradictory tastes. The system shows how recommenders can produce unexpected results when facing inputs that don't align with typical patterns in the training data.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

```

## Terminal Output

### main.py
```bash
Loaded 18 songs from data/songs.csv
Using profile: chill_lofi_lover
  Favorite Genre: lofi
  Favorite Mood: chill
  Target Energy: 0.4
  Likes Acoustic: True


Top recommendations:

Library Rain - Score: 0.98
Because: Recommended because:
- Genre matches your preference (lofi)
- Mood matches your preference (chill)
- Energy is very close to your target (0.35 vs 0.4)
- High acousticness fits your preference (0.86)

Final score: 0.979 / 1.0

Midnight Coding - Score: 0.96
Because: Recommended because:
- Genre matches your preference (lofi)
- Mood matches your preference (chill)
- Energy is very close to your target (0.42 vs 0.4)
- High acousticness fits your preference (0.71)

Final score: 0.957 / 1.0

Focus Flow - Score: 0.83
Because: Recommended because:
- Genre matches your preference (lofi)
- Energy is very close to your target (0.40 vs 0.4)
- High acousticness fits your preference (0.78)

Final score: 0.833 / 1.0

Spacewalk Thoughts - Score: 0.59
Because: Recommended because:
- Mood matches your preference (chill)
- Energy is reasonably close to your target (0.28 vs 0.4)
- High acousticness fits your preference (0.92)

Final score: 0.595 / 1.0

Coffee Shop Stories - Score: 0.55
Because: Recommended because:
- Energy is very close to your target (0.37 vs 0.4)
- High acousticness fits your preference (0.89)

Final score: 0.553 / 1.0
```

### test_edge_cases.py
```bash
Loaded 18 songs from data/songs.csv
================================================================================
EDGE CASE TEST: PARADOXICAL_HIGH_ENERGY_ACOUSTIC
================================================================================

📊 Profile Configuration:
   Favorite Genre: pop
   Favorite Mood: happy
   Target Energy: 0.95
   Likes Acoustic: True
   Target Tempo: 130 BPM
   Target Valence: 0.85
   Target Danceability: 0.85
   Target Acousticness: 0.9

⚠️  Potential Contradictions:
   • HIGH ENERGY (0.95) but WANTS ACOUSTIC (0.90)
   • Acoustic music typically has LOW energy
   • This profile wants impossible combination

🎵 Top 5 Recommendations:
--------------------------------------------------------------------------------

1. Sunrise City by Neon Echo
   Genre: pop, Mood: happy
   Energy: 0.82, Tempo: 118 BPM
   Valence: 0.84, Danceability: 0.79
   Acousticness: 0.18
   ⭐ Score: 0.8333
   Match Analysis:
      Genre: ✓, Mood: ✓
      Energy diff: 0.13, Tempo diff: 12 BPM
      ⚠️  High energy but LOW acoustic (contradicts preference)
   Recommended because:
- Genre matches your preference (pop)
- Mood matches your preference (happy)
- Energy is reasonably close to your target (0.82 vs 0.95)

Final score: 0.833 / 1.0

2. Gym Hero by Max Pulse
   Genre: pop, Mood: intense
   Energy: 0.93, Tempo: 132 BPM
   Valence: 0.77, Danceability: 0.88
   Acousticness: 0.05
   ⭐ Score: 0.7165
   Match Analysis:
      Genre: ✓, Mood: ✗
      Energy diff: 0.02, Tempo diff: 2 BPM
      ⚠️  High energy but LOW acoustic (contradicts preference)
   Recommended because:
- Genre matches your preference (pop)
- Energy is very close to your target (0.93 vs 0.95)

Final score: 0.717 / 1.0

3. Rooftop Lights by Indigo Parade
   Genre: indie pop, Mood: happy
   Energy: 0.76, Tempo: 124 BPM
   Valence: 0.81, Danceability: 0.82
   Acousticness: 0.35
   ⭐ Score: 0.5389
   Match Analysis:
      Genre: ✗, Mood: ✓
      Energy diff: 0.19, Tempo diff: 6 BPM
   Recommended because:
- Mood matches your preference (happy)
- Energy is reasonably close to your target (0.76 vs 0.95)

Final score: 0.539 / 1.0

4. Electric Pulse by Cyber Beat
   Genre: electronic, Mood: energetic
   Energy: 0.89, Tempo: 128 BPM
   Valence: 0.86, Danceability: 0.91
   Acousticness: 0.12
   ⭐ Score: 0.4457
   Match Analysis:
      Genre: ✗, Mood: ✗
      Energy diff: 0.06, Tempo diff: 2 BPM
      ⚠️  High energy but LOW acoustic (contradicts preference)
   Recommended because:
- Energy is very close to your target (0.89 vs 0.95)

Final score: 0.446 / 1.0

5. Storm Runner by Voltline
   Genre: rock, Mood: intense
   Energy: 0.91, Tempo: 152 BPM
   Valence: 0.48, Danceability: 0.66
   Acousticness: 0.10
   ⭐ Score: 0.2958
   Match Analysis:
      Genre: ✗, Mood: ✗
      Energy diff: 0.04, Tempo diff: 22 BPM
      ⚠️  High energy but LOW acoustic (contradicts preference)
   Recommended because:
- Energy is very close to your target (0.91 vs 0.95)

Final score: 0.296 / 1.0

📈 Score Distribution Analysis:
   Average score across all songs: 0.3066
   Maximum score: 0.8333
   Minimum score: 0.1516
   Score range: 0.6817


================================================================================
EDGE CASE TEST: IMPOSSIBLE_SLOW_METAL
================================================================================

📊 Profile Configuration:
   Favorite Genre: rock
   Favorite Mood: intense
   Target Energy: 0.15
   Likes Acoustic: False
   Target Tempo: 50 BPM
   Target Valence: 0.2
   Target Danceability: 0.2
   Target Acousticness: 0.1

⚠️  Potential Contradictions:
   • ROCK/INTENSE genre but LOW ENERGY (0.15)
   • SLOW TEMPO (50 BPM) for intense rock
   • Rock/intense music typically has HIGH energy and FAST tempo

🎵 Top 5 Recommendations:
--------------------------------------------------------------------------------

1. Storm Runner by Voltline
   Genre: rock, Mood: intense
   Energy: 0.91, Tempo: 152 BPM
   Valence: 0.48, Danceability: 0.66
   Acousticness: 0.10
   ⭐ Score: 0.7791
   Match Analysis:
      Genre: ✓, Mood: ✓
      Energy diff: 0.76, Tempo diff: 102 BPM
   Recommended because:
- Genre matches your preference (rock)
- Mood matches your preference (intense)
- Low acousticness fits your preference (0.10)

Final score: 0.779 / 1.0

2. Gym Hero by Max Pulse
   Genre: pop, Mood: intense
   Energy: 0.93, Tempo: 132 BPM
   Valence: 0.77, Danceability: 0.88
   Acousticness: 0.05
   ⭐ Score: 0.4077
   Match Analysis:
      Genre: ✗, Mood: ✓
      Energy diff: 0.78, Tempo diff: 82 BPM
   Recommended because:
- Mood matches your preference (intense)
- Low acousticness fits your preference (0.05)

Final score: 0.408 / 1.0

3. Night Drive Loop by Neon Echo
   Genre: synthwave, Mood: moody
   Energy: 0.75, Tempo: 110 BPM
   Valence: 0.49, Danceability: 0.73
   Acousticness: 0.22
   ⭐ Score: 0.3139
   Match Analysis:
      Genre: ✗, Mood: ✗
      Energy diff: 0.60, Tempo diff: 60 BPM
   Recommended because:
- Low acousticness fits your preference (0.22)

Final score: 0.314 / 1.0

4. Heavy Thunder by Dark Forge
   Genre: metal, Mood: angry
   Energy: 0.95, Tempo: 145 BPM
   Valence: 0.25, Danceability: 0.58
   Acousticness: 0.08
   ⭐ Score: 0.2940
   Match Analysis:
      Genre: ✗, Mood: ✗
      Energy diff: 0.80, Tempo diff: 95 BPM
   Recommended because:
- Low acousticness fits your preference (0.08)

Final score: 0.294 / 1.0

5. Sunrise City by Neon Echo
   Genre: pop, Mood: happy
   Energy: 0.82, Tempo: 118 BPM
   Valence: 0.84, Danceability: 0.79
   Acousticness: 0.18
   ⭐ Score: 0.2381
   Match Analysis:
      Genre: ✗, Mood: ✗
      Energy diff: 0.67, Tempo diff: 68 BPM
   Recommended because:
- Low acousticness fits your preference (0.18)

Final score: 0.238 / 1.0

📈 Score Distribution Analysis:
   Average score across all songs: 0.2442
   Maximum score: 0.7791
   Minimum score: 0.0770
   Score range: 0.7022


================================================================================
EDGE CASE TEST: HYPER_FAST_AMBIENT
================================================================================

📊 Profile Configuration:
   Favorite Genre: ambient
   Favorite Mood: chill
   Target Energy: 0.8
   Likes Acoustic: True
   Target Tempo: 180 BPM
   Target Valence: 0.7
   Target Danceability: 0.75
   Target Acousticness: 0.85

⚠️  Potential Contradictions:
   • AMBIENT/CHILL genre but HIGH ENERGY (0.80)
   • VERY FAST TEMPO (180 BPM) for ambient music
   • Ambient/chill music typically has LOW energy and SLOW tempo

🎵 Top 5 Recommendations:
--------------------------------------------------------------------------------

1. Spacewalk Thoughts by Orbit Bloom
   Genre: ambient, Mood: chill
   Energy: 0.28, Tempo: 60 BPM
   Valence: 0.65, Danceability: 0.41
   Acousticness: 0.92
   ⭐ Score: 0.7998
   Match Analysis:
      Genre: ✓, Mood: ✓
      Energy diff: 0.52, Tempo diff: 120 BPM
   Recommended because:
- Genre matches your preference (ambient)
- Mood matches your preference (chill)
- High acousticness fits your preference (0.92)

Final score: 0.800 / 1.0

2. Library Rain by Paper Lanterns
   Genre: lofi, Mood: chill
   Energy: 0.35, Tempo: 72 BPM
   Valence: 0.60, Danceability: 0.58
   Acousticness: 0.86
   ⭐ Score: 0.4770
   Match Analysis:
      Genre: ✗, Mood: ✓
      Energy diff: 0.45, Tempo diff: 108 BPM
   Recommended because:
- Mood matches your preference (chill)
- High acousticness fits your preference (0.86)

Final score: 0.477 / 1.0

3. Symphony No. 5 by Orchestra One
   Genre: classical, Mood: dramatic
   Energy: 0.72, Tempo: 68 BPM
   Valence: 0.38, Danceability: 0.32
   Acousticness: 0.94
   ⭐ Score: 0.4703
   Match Analysis:
      Genre: ✗, Mood: ✗
      Energy diff: 0.08, Tempo diff: 112 BPM
   Recommended because:
- Energy is very close to your target (0.72 vs 0.8)
- High acousticness fits your preference (0.94)

Final score: 0.470 / 1.0

4. Midnight Coding by LoRoom
   Genre: lofi, Mood: chill
   Energy: 0.42, Tempo: 78 BPM
   Valence: 0.56, Danceability: 0.62
   Acousticness: 0.71
   ⭐ Score: 0.4061
   Match Analysis:
      Genre: ✗, Mood: ✓
      Energy diff: 0.38, Tempo diff: 102 BPM
   Recommended because:
- Mood matches your preference (chill)
- High acousticness fits your preference (0.71)

Final score: 0.406 / 1.0

5. Mountain Trail by Whispering Pines
   Genre: folk, Mood: peaceful
   Energy: 0.32, Tempo: 72 BPM
   Valence: 0.78, Danceability: 0.45
   Acousticness: 0.88
   ⭐ Score: 0.3475
   Match Analysis:
      Genre: ✗, Mood: ✗
      Energy diff: 0.48, Tempo diff: 108 BPM
   Recommended because:
- High acousticness fits your preference (0.88)

Final score: 0.348 / 1.0

📈 Score Distribution Analysis:
   Average score across all songs: 0.3114
   Maximum score: 0.7998
   Minimum score: 0.1729
   Score range: 0.6269


================================================================================
EDGE CASE TESTING COMPLETE
================================================================================

🔍 Key Observations:
   • Check if the recommender found any songs matching impossible criteria
   • Look at score distribution - are scores suspiciously low?
   • See which features the recommender prioritized
   • Identify if any songs 'tricked' the system with high scores
```

