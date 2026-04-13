# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**  

---

## 2. Intended Use  

This system suggests 3 to 5 songs from a catalog of 18 tracks based on user preferences. It considers the user's favorite genre, mood, and energy level to generate personalized recommendations. The system targets classroom exploration and learning purposes, not real-world users.  

---

## 3. How the Model Works  

The system evaluates songs using seven features: genre, mood, energy, tempo, valence, danceability, and acousticness. It compares each song feature to the user's preferences using a scoring approach. For categorical features like genre and mood, it gives full points for an exact match. For numerical features like energy and tempo, it uses a mathematical function that rewards closeness to the target value. The system combines these scores using weighted percentages to produce a final score between 0 and 1. This approach differs from simple difference scoring by ensuring songs closer to user preferences score higher, regardless of whether values are higher or lower.

---

## 4. Data  

The system uses a catalog of 18 songs stored in `data/songs.csv`. The dataset represents seven genres: pop, lofi, rock, jazz, ambient, synthwave, and indie pop. It includes six mood categories: happy, chill, intense, relaxed, moody, and angry. The data reflects a curated selection of fictional songs with consistent audio feature measurements. The catalog lacks diversity in sub-genres and does not include lyrics, language, or cultural context.  

---

## 5. Strengths  

The system works well for users with clear, consistent preferences. It accurately recommends songs that match both genre and mood while staying close to target energy levels. The scoring captures the intuition that songs with similar characteristics should rank higher. The system provides transparent explanations for each recommendation, showing exactly which features matched. It handles standard profiles like chill lofi lovers and energetic pop fans effectively.  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The system over-prioritizes categorical features (genre and mood) which together account for 40% of the total score, allowing songs to achieve high recommendations even when numerical preferences like energy, tempo, and acousticness are completely contradictory to the user's targets. This means the recommender can be "tricked" by profiles with impossible combinations, such as requesting high-energy acoustic music or slow-tempo intense rock, because the scoring logic treats each feature independently without validating whether preference combinations make realistic sense in actual music. The Gaussian similarity function for numerical features is also relatively forgiving, meaning large differences from target values still yield moderate scores, further reducing the system's sensitivity to contradictory user preferences.

---

## 7. Evaluation 

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

I tested seven standard profiles including chill_lofi_lover, energetic_pop_fan, and intense_rocker, plus three edge-case profiles designed with contradictory preferences. I examined whether the recommender could find songs matching impossible combinations like high-energy acoustic music or slow-tempo intense rock. The results surprised me because the system gave high scores to songs that matched genre and mood perfectly, even when numerical features like energy and tempo were completely opposite to the user's targets. For example, a rock song with energy 0.91 scored highly for a profile requesting energy 0.15, simply because it matched the rock genre and intense mood. I also ran score distribution analysis which showed average scores were low (0.24-0.31) but maximum scores remained high (0.78-0.83), revealing that categorical matching dominates the scoring logic.

---

## 8. Future Work  

I would add consistency validation to detect and flag contradictory preferences before processing recommendations. I would implement feature correlation awareness to understand typical relationships between musical features. I would add support for multiple users and group recommendations. I would improve diversity among top results instead of always picking the closest match. I would incorporate additional features like tempo ranges and lyric themes. I would add more songs across diverse genres and cultural styles.  

---

## 9. Personal Reflection  

I learned that recommender systems turn complex user preferences into simple numerical scores. I discovered that even simple systems can exhibit unexpected behaviors when facing contradictory inputs. This project showed me that human judgment remains essential for validating recommendations. Building this system changed how I think about music apps. I now understand the challenges of balancing different features and the importance of transparency in recommendation algorithms.  
