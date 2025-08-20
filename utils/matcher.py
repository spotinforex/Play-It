from rapidfuzz import fuzz
import logging

logging.basicConfig(level=logging.INFO)

def search_and_match(yt, track):
    try:
        logging.info("Matching Songs In Progress")

        # Build search query
        query = f"{track['title']} {track['artist']}"

        # YouTube search request
        request = yt.search().list(
            part="snippet",
            q=query,
            maxResults=5,
            type="video"
        )
        response = request.execute()

        best_match = None
        best_score = 0

        for item in response.get("items", []):
            video_title = item["snippet"]["title"]
            score = fuzz.token_set_ratio(video_title, query)

            if score > best_score:
                best_match = item["id"]["videoId"]
                best_score = score   # ✅ update the score too

        logging.info(f"Best match score: {best_score}")
        return best_match if best_score >= 70 else None

    except Exception as e:
            logging.exception("An Error Occurred While Matching Songs")

