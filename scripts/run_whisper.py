import argparse
import logging
import os
import time

import numpy as np
import pandas as pd
import whisper


def clean_channel_title(channel_title):
    """Clean channel title by removing capital letters and spaces."""
    return channel_title.lower().replace(" ", "_")


def process_audio_file(channel_title, ep_number, new_ep):
    """Process a single audio file."""
    # Get absolute path of directory containing the script.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get audio and output file paths.
    audio_file_path = os.path.join(script_dir, f'audio/{channel_title}/{ep_number}.m4a')
    out_file_path = os.path.join(script_dir, f'audio_transcription/{channel_title}/0{ep_number}.txt')

    # Skip if output file already exists.
    if os.path.exists(out_file_path):
        print(f"Skipping existing file: {out_file_path}")
        logging.info(f"Skipping existing file: {out_file_path}")
        return

    # Load Whisper model and transcribe audio file.
    print(f"Processing file: {audio_file_path}")
    logging.info(f"Processing file: {audio_file_path}")
    start_time = time.time()
    try:
        model = whisper.load_model("medium")
        result = model.transcribe(audio_file_path)
    except RuntimeError as e:
        print(f"Error processing file {audio_file_path}: {str(e)}")
        logging.error(f"Error processing file {audio_file_path}: {str(e)}")
        return

    # Write transcription to output file.
    with open(out_file_path, "w") as f:
        for seg in result["segments"]:
            ts = np.round(seg["start"], 1)
            f.write(f"{new_ep.loc[ep_number, 'link']}&t={ts}s\t{str(ts)}\t{seg['text']}\n")

    end_time = time.time()
    time_diff = end_time - start_time
    print(f"Time taken: {time_diff:.2f} seconds")
    logging.info(f"File processed: {audio_file_path}")
    logging.info(f"Time taken: {time_diff:.2f} seconds")


def process_channel(channel_title):
    """Process all audio files for a given channel."""
    # Read csv file with episode metadata.
    eps_file_path = f"audio_transcription/{channel_title}/episodes.csv"
    new_ep = pd.read_csv(eps_file_path, index_col=None)

    # Clean channel title.
    if any(c.isupper() for c in channel_title) or " " in channel_title:
        channel_title = clean_channel_title(channel_title)

    # Process each audio file.
    for ix in new_ep.index:
        print(f"EPISODE: {ix}")
        logging.info("EPISODE: %s", ix)
        process_audio_file(channel_title, ix, new_ep)


def main():
    """The main function of the program."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel_title", type=str)
    args = parser.parse_args()

    # Process channel.
    process_channel(args.channel_title)


if __name__ == "__main__":
    main()