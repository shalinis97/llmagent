# Phase B: LLM-based Automation Agent for DataWorks Solutions

# B1 & B2: Security Checks
import os
import subprocess


def B12(filepath):
    if filepath.startswith('/data'):
        # raise PermissionError("Access outside /data is not allowed.")
        # print("Access outside /data is not allowed.")
        return True
    else:
        return False

# B3: Fetch Data from an API
def B3(url, save_path):
    if not B12(save_path):
        return None
    import requests
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)

#B4

def B4(repo_url, commit_message="Automated commit", file_path="README.md", content="Updated via automation"):
    """
    Clones a Git repository, makes a commit, and optionally pushes the changes.

    :param repo_url: URL of the Git repository.
    :param commit_message: Commit message.
    :param file_path: File to modify or create inside the repo.
    :param content: Content to write into the file.
    :return: Success or failure message.
    """
    try:
        # Extract repo name
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        clone_dir = f"/data/{repo_name}"  # Clone into /data directory

        # Clone the repo
        if os.path.exists(clone_dir):
            print(f"Repository already exists at {clone_dir}. Pulling latest changes...")
            subprocess.run(["git", "-C", clone_dir, "pull"], check=True)
        else:
            print(f"Cloning repository {repo_url}...")
            subprocess.run(["git", "clone", repo_url, clone_dir], check=True)

        # Create or modify a file inside the cloned repo
        file_path = os.path.join(clone_dir, file_path)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        # Stage and commit changes
        subprocess.run(["git", "-C", clone_dir, "add", file_path], check=True)
        subprocess.run(["git", "-C", clone_dir, "commit", "-m", commit_message], check=True)

        print("✅ Changes committed successfully.")

        # Optionally push the changes (requires credentials or SSH access)
        # subprocess.run(["git", "-C", clone_dir, "push"], check=True)

        return f"Repository {repo_url} updated successfully."
    except subprocess.CalledProcessError as e:
        return f"Error in Git operation: {e}"


# B5: Run SQL Query
def B5(db_path, query, output_filename):
    if not B12(db_path):
        return None
    import sqlite3, duckdb
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result

# B6: Web Scraping
def B6(url, output_filename):
    import requests
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))

# B7: Image Processing
def B7(image_path, output_path, resize=None):
    from PIL import Image
    if not B12(image_path):
        return None
    if not B12(output_path):
        return None
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)


def B8(audio_path):
    """
    Transcribes an audio file to text using Whisper (local model).
    
    :param audio_path: Path to the audio file.
    :return: Transcribed text or None if an error occurs.
    """
    # Validate if the file exists
    if not os.path.exists(audio_path):
        print(f"Error: File '{audio_path}' does not exist.")
        return None

    try:
        # Load the Whisper model (use 'base', 'small', 'medium', or 'large' as needed)
        model = whisper.load_model("base")

        # Transcribe the audio
        result = model.transcribe(audio_path)

        return result["text"]  # Extract only the transcribed text
    
    except Exception as e:
        print(f"Error in transcription: {e}")
        return None

# B9: Markdown to HTML Conversion
import markdown


def B9(markdown_file, output_file=None):
    """
    Converts a Markdown file to HTML.

    :param markdown_file: Path to the Markdown (.md) file.
    :param output_file: Path to save the HTML file (optional).
    :return: HTML content as a string.
    """
    # Validate if the file exists
    if not os.path.exists(markdown_file):
        print(f"Error: File '{markdown_file}' does not exist.")
        return None

    try:
        # Read Markdown content
        with open(markdown_file, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()

        # Convert Markdown to HTML
        html_content = markdown.markdown(md_content)

        # Determine output file if not provided
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

# B10: API Endpoint for CSV Filtering
import pandas as pd
import os
import json

def B10(csv_file, filter_column, filter_value):
    """
    Filters a CSV file based on a column and value, returns JSON.

    :param csv_file: Path to the CSV file.
    :param filter_column: Column name to filter on.
    :param filter_value: Value to filter.
    :return: JSON string of the filtered data.
    """
    # Validate if the file exists
    if not os.path.exists(csv_file):
        print(f"Error: File '{csv_file}' does not exist.")
        return None

    try:
        # Load the CSV
        df = pd.read_csv(csv_file)

        # Check if the column exists
        if filter_column not in df.columns:
            print(f"Error: Column '{filter_column}' not found in {csv_file}")
            return None

        # Filter data
        filtered_df = df[df[filter_column] == filter_value]

        # Convert to JSON
        json_output = filtered_df.to_json(orient="records", indent=4)

        return json_output
    except Exception as e:
        print(f"Error in filtering CSV: {e}")
        return None