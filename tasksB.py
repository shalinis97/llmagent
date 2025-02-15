# Phase B: LLM-based Automation Agent for DataWorks Solutions

# B1 & B2: Security Checks
import os
import subprocess

def B12(filepath):
    """
    Helper function to enforce:
    - B1: Only access /data
    - B2: Do not delete data (we do not delete inside tasks here).
    
    Returns True if filepath starts with /data, otherwise False.
    """
    if filepath.startswith('/data'):
        return True
    else:
        return False

# B3: Fetch Data from an API
def B3(url, save_path):
    """
    Fetch data from an API endpoint and save it to a file in /data.
    """
    if not B12(save_path):
        print("Access outside /data is not allowed.")
        return None

    import requests
    response = requests.get(url)
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(response.text)
    print(f"Fetched data from {url} and saved to {save_path}")

# B4: Clone a Git Repo and Make a Commit
def B4(repo_url, commit_message="Automated commit",
       file_path="README.md", content="Updated via automation"):
    """
    Clones a Git repository into /data, modifies or creates a file,
    then commits (and optionally pushes) the changes.
    """
    try:
        # Extract repo name
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        clone_dir = f"/data/{repo_name}"  # Must be in /data

        # Clone the repo (or pull if it exists)
        if os.path.exists(clone_dir):
            print(f"Repository already exists at {clone_dir}. Pulling latest changes...")
            subprocess.run(["git", "-C", clone_dir, "pull"], check=True)
        else:
            print(f"Cloning repository {repo_url} into {clone_dir}...")
            subprocess.run(["git", "clone", repo_url, clone_dir], check=True)

        # Create or modify the specified file inside the cloned repo
        full_file_path = os.path.join(clone_dir, file_path)
        if not B12(full_file_path):
            print("Access outside /data is not allowed.")
            return None

        with open(full_file_path, "w", encoding="utf-8") as file:
            file.write(content)

        # Stage and commit changes
        subprocess.run(["git", "-C", clone_dir, "add", file_path], check=True)
        subprocess.run(["git", "-C", clone_dir, "commit", "-m", commit_message], check=True)

        print("✅ Changes committed successfully.")

        # If pushing is desired and you have credentials/SSH configured, uncomment:
        # subprocess.run(["git", "-C", clone_dir, "push"], check=True)

        return f"Repository {repo_url} updated successfully."
    except subprocess.CalledProcessError as e:
        print(f"Error in Git operation: {e}")
        return None

# B5: Run a SQL Query on SQLite or DuckDB
def B5(db_path, query, output_filename):
    """
    Runs a provided SQL query on either a SQLite or DuckDB database
    (determined by file extension) and writes the result to an output file.
    """
    if not B12(db_path):
        print("Access outside /data is not allowed.")
        return None
    if not B12(output_filename):
        print("Access outside /data is not allowed.")
        return None

    import sqlite3
    import duckdb

    # Choose sqlite3 if db_path ends with .db, else duckdb
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()

    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(str(result))

    print(f"Query '{query}' executed; results written to {output_filename}")
    return result

# B6: Scrape (Extract) Data from a Website
def B6(url, output_filename):
    """
    Fetches the HTML content at the given URL and writes it to output_filename.
    """
    if not B12(output_filename):
        print("Access outside /data is not allowed.")
        return None

    import requests
    result = requests.get(url).text
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(result)
    print(f"Scraped {url} and saved content to {output_filename}")

# B7: Compress or Resize an Image
def B7(image_path, output_path, resize=None):
    """
    Opens an image, optionally resizes it, and saves it to output_path.
    """
    if not B12(image_path):
        print("Access outside /data is not allowed.")
        return None
    if not B12(output_path):
        print("Access outside /data is not allowed.")
        return None

    from PIL import Image
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)
    print(f"Image {image_path} processed and saved to {output_path}")

# B8: Transcribe Audio from an MP3 file
def B8(audio_path):
    """
    Transcribes an audio file to text using a local Whisper model.
    Returns the transcribed text, or None if an error occurs.
    
    This example references 'whisper' (OpenAI's Whisper library), which
    you would need installed locally or replaced with your own method.
    """
    if not os.path.exists(audio_path):
        print(f"Error: File '{audio_path}' does not exist.")
        return None
    if not B12(audio_path):
        print("Access outside /data is not allowed.")
        return None

    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        print(f"Transcription of {audio_path} completed.")
        return result["text"]
    except Exception as e:
        print(f"Error in transcription: {e}")
        return None

# B9: Convert Markdown to HTML
import markdown
def B9(markdown_file, output_file=None):
    """
    Converts a Markdown file to HTML.
    If output_file is not provided, uses the same name with .html extension.
    Returns the HTML content as a string, or None on error.
    """
    if not B12(markdown_file):
        print("Access outside /data is not allowed.")
        return None

    if output_file is not None and not B12(output_file):
        print("Access outside /data is not allowed.")
        return None

    if not os.path.exists(markdown_file):
        print(f"Error: File '{markdown_file}' does not exist.")
        return None

    try:
        # Read Markdown content
        with open(markdown_file, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()

        # Convert Markdown to HTML
        html_content = markdown.markdown(md_content)

        # If no output file provided, replace .md with .html
        if output_file is None:
            output_file = markdown_file.replace(".md", ".html")

        # Save the HTML output
        with open(output_file, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

        print(f"Markdown converted to HTML: {output_file}")
        return html_content
    except Exception as e:
        print(f"Error in Markdown to HTML conversion: {e}")
        return None

# B10: Write an API Endpoint (or function) that filters a CSV file and returns JSON
import pandas as pd
import json

def B10(csv_file, filter_column, filter_value):
    """
    Filters a CSV file based on a given column/value and returns the matching rows in JSON.
    """
    if not B12(csv_file):
        print("Access outside /data is not allowed.")
        return None

    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' does not exist.")
        return None

    try:
        df = pd.read_csv(csv_file)

        # Ensure the column exists
        if filter_column not in df.columns:
            print(f"Error: Column '{filter_column}' not found in {csv_file}")
            return None

        # Filter
        filtered_df = df[df[filter_column] == filter_value]

        # Convert to JSON (records format)
        json_output = filtered_df.to_json(orient="records", indent=4)

        print(f"Filtered {csv_file} on {filter_column}={filter_value}")
        return json_output
    except Exception as e:
        print(f"Error in filtering CSV: {e}")
        return None
