import time
from app.services.trends import fetch_google_trending_keywords

start = time.time()

trends = fetch_google_trending_keywords("fitness")

end = time.time()

print("Time taken:", round(end - start, 2), "seconds")
print("Number of results:", len(trends))
print("Sample:", trends[:3])