
from rest_framework import viewsets
from django.shortcuts import render, redirect
from .models import Video
from .serializer import VideoSerializer
from django.test import TestCase
import subprocess
import imageio
import sys
from rest_framework.decorators import api_view, action
import pysrt
import cv2, os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from rest_framework.response import Response
import json
import requests
from django.http import JsonResponse
import boto3
import logging
from storages.backends.s3boto3 import S3Boto3Storage
import uuid
boto3.set_stream_logger('boto3', level=logging.DEBUG)
class VideoModelViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    def create(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode('utf-8'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        file_path = json_data.get('file', '')
        searched_key = json_data.get('searched_key', '')
        id_file = json_data.get('id', '')
        data = request.data
        if(searched_key=='null'):
            print("Execution of if block")
            execute(file_path, data)
            
            
        # Return JSON response
            return JsonResponse({'message': 'Success', 'data': json_data})
        else:
            print("Execution of else block")
            send_to_dynamodb(searched_key,id_file)
            
            timestamps = search_keyword(searched_key,request)
            json_data = {'results': timestamps}
            return JsonResponse({'error': 'An error occurred'})
            
        




def send_to_dynamodb(searched_key,id):
    session = boto3.Session(
    aws_access_key_id='AKIA4MTWI634VE2MBC4N',
    aws_secret_access_key='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',
    region_name='us-east-2'
)

# Use the session to create a DynamoDB client
    dynamodb = session.client('dynamodb')

# Print AWS credentials
    credentials = session.get_credentials()
    print(credentials.access_key)
    print(credentials.secret_key)
    print(credentials.token)

# Specify the DynamoDB table name
    table_name = 'search'

# Data to be sent to DynamoDB
    data_to_send = {
    'id': uuid.uuid4(),
    'search_key': searched_key,  # Replace with the actual value you want to store
    # Add more key-value pairs as needed
    }

    try:
    # Put item in the DynamoDB table
        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                   'id': {'S': str(data_to_send['id'])},  # Convert number to string for 'N' type
                    'search_key': {'S': data_to_send['search_key']},
            }
         )

    # Optionally, handle the response
        print(response)

    except Exception as e:
    # Handle exceptions, log errors, etc.
        print(f"Error sending data to DynamoDB: {e}")
        
   

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


          
def search_keyword(searched_key,request):
    srt_file_path = 'outputfile1.srt'
    keyword_to_search = searched_key
    timestamps = get_timestamps_for_keyword(srt_file_path, keyword_to_search)

    if timestamps:
        
        for index, timestamp in enumerate(timestamps, 1):
            print(f"Subtitle {index}: Timestamp - {timestamp}")
        return timestamps
    else:
        print(f"No subtitles found for the keyword '{keyword_to_search}'.")        
    return render(request, 'search_results.html', {'results': []})


def execute(file_path, data):
        file_path= file_path.replace(' ', '_')
        subprocess.run(['CCExtractor_win_portable\ccextractorwinfull.exe',file_path,'-o','outputfile1.srt'])
        srtfilename = "outputfile1.srt"
        mp4filename =  file_path
        count = 0
        cap = cv2.VideoCapture(file_path)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        print(f'Checking Video {count} Frames {frames} fps: {fps} url:{file_path}')
        try:
            print("********************Running******************************************")
            
            seralizer = VideoSerializer(data = data)
            if seralizer.is_valid():
                seralizer.save()
                print(seralizer.data)
                video = VideoFileClip(file_path)
                subtitles = pysrt.open(srtfilename)
                begin,end= mp4filename.split(".mp4")
                output_video_file = begin+'_subtitled'+".mp4"
                print ("Output file name: ",output_video_file)
                print("********************Running btwen******************************************")

                # Create subtitle clips
                subtitle_clips = create_subtitle_clips(subtitles,video.size)

                # Add subtitles to the video
                final_video = CompositeVideoClip([video] + subtitle_clips)

                # Write output video file
                final_video.write_videofile(output_video_file)
                #send to s3
                local_file_path = output_video_file
                s3_bucket = 'ccextractorproject'
                s3_object_key = local_file_path
                
                
                upload_to_s3(local_file_path, s3_bucket, s3_object_key)
            

                
                return Response({
                    'status' : True,
                    'message' : 'success',
                    'data' : seralizer.data
                 })
            else :
                return Response({

                'status' : False,
                'message' : "all Fields Required",
                'data' : seralizer.errors
            })
        except Exception as e:
            print(e)

import boto3




def time_to_seconds(time_obj):
    return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000


def create_subtitle_clips(subtitles, videosize,fontsize=24, font='Arial', color='yellow', debug = False):
    subtitle_clips = []

    for subtitle in subtitles:
        start_time = time_to_seconds(subtitle.start)
        end_time = time_to_seconds(subtitle.end)
        duration = end_time - start_time

        video_width, video_height = videosize
        
        text_clip = TextClip(subtitle.text, fontsize=fontsize, font=font, color=color, bg_color = 'black',size=(video_width*3/4, None), method='caption').set_start(start_time).set_duration(duration)
        subtitle_x_position = 'center'
        subtitle_y_position = video_height* 4 / 5 

        text_position = (subtitle_x_position, subtitle_y_position)                    
        subtitle_clips.append(text_clip.set_position(text_position))

    return subtitle_clips



   
    
def upload_to_s3(local_file_path, s3_bucket, s3_object_key):
    # Set up AWS credentials and region (ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are in your environment)
    s3 = S3Boto3Storage()

    try:
        print(f"local file path {local_file_path} s3bucket {s3_bucket} s3 object key {s3_object_key}")
        # Upload the file to S3
        s3.save(s3_object_key, open(local_file_path, 'rb'))
        print(f"File uploaded successfully to S3: s3://{s3_bucket}/{s3_object_key}")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")






