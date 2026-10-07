# Simple tool used to download youtube mp3's & mp4's
# You have to install  ffmpeg

import yt_dlp 

def search_youtube(query,max_results= 10):
    # Search YT and return a list of dicts
    search_query = f"ytsearch{max_results}:{query}"

    opts = {
        "quiet": True,
        "extract_flat": True, 
        "skip_download": True,
        "cookiesfrombrowser": ("edge",),
          }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(search_query, download=False)
        return info.get("entries", [])


def download_audio(url, output_folder= "."):
    # Download audio from a given URL
    opts = {
        "format": "bestaudio/best",
    
        "postprocessors": [
            {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
            }
        ],
        "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
        "quiet": False ,
        "cookiesfrombrowser": ("edge",),
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

def main():
    query = input("Enter song name: ").strip()

    if not query:
        print("Nothing typed.")
        return

    #max_results = int(count_input) if count_input.isdigit() else 5


    print(f"\n Searching YouTube for {query}\n")
    results = search_youtube(query)

    if not results:
        print("No results found.")
        return

    for i, entry in enumerate(results, start=1):
        title= entry.get("title", "Unknown Title")
        duration = entry.get("duration")
        duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown Duration"  

        uploader = entry.get("uploader", "Unknown channel") 
        print(f"{i}. {title} ({duration_str}) - {uploader}")

    choice = input(f"\n Pick a number (1-{len(results)}), or 'q' to quit: ").strip()

    if choice.lower() == 'q':
        return

    try:
        choice_index= int(choice)- 1
        if choice_index < 0 or choice_index >= len(results):
            raise ValueError
    except ValueError:
        print("Invalid choice.")
        return

    selected = results[choice_index]
    url = selected.get("url") or f"https://youtube.com/watch?v={selected['id']}"

    print(f"\n Downloading : {selected.get('title')}")
    download_audio(url)

if __name__ == "__main__":
    main()