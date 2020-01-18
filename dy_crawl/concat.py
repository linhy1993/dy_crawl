import glob
from datetime import datetime

from moviepy.editor import *

from dy_crawl.settings import Config


def concat_mp4():
    print("[INFO] Start concating mp4 under ouput folder")
    mp4s = glob.glob(os.path.join(Config.OUTPUT_PATH, "*.mp4"))
    clip_lst = [VideoFileClip(mp4) for mp4 in mp4s]
    new_file_location = str(os.path.join(Config.BASEDIR, f'{str(datetime.now())}.mp4'))
    final_clip = concatenate_videoclips(clip_lst, method='compose')
    final_clip.write_videofile(new_file_location)
