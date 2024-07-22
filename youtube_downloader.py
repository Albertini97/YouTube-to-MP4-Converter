import os
import requests
from pytube import YouTube
from flask import request, redirect, url_for, flash, send_file
import tempfile
import shutil

def download_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
    if not stream:
        return None
    temp_dir = tempfile.mkdtemp()
    download_path = stream.download(output_path=temp_dir)
    return download_path