
def get_timestamps_for_keyword(srt_file_path, keyword):
    timestamps = []

    try:
        with open(srt_file_path, 'r') as file:
            lines = file.read().split('\n\n')

            for block in lines:
                if keyword.lower() in block.lower():
                    timestamp_line = block.split('\n', 1)[1].split('\n', 1)[0]
                    timestamps.append(timestamp_line)

    except FileNotFoundError:
        print(f"Error: File not found - {srt_file_path}")
    except Exception as e:
        print(f"Error reading file: {e}")

    return timestamps

# Example usage:
srt_file_path = 'outputfile1.srt'
keyword_to_search = '''ACTUALLY, I WAS,                
LIKE, CHEERING                  
THE NAME OF THE SCHOOL.'''
timestamps = get_timestamps_for_keyword(srt_file_path, keyword_to_search)

if timestamps:
    for index, timestamp in enumerate(timestamps, 1):
        print(f"Subtitle {index}: Timestamp - {timestamp}")
else:
    print(f"No subtitles found for the keyword '{keyword_to_search}'.")        

