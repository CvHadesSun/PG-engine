'''
Date: 2022-01-19 15:49:08
LastEditors: cvhadessun
LastEditTime: 2022-02-10 10:33:39
FilePath: /PG-engine/run/demo/demo_smplx_new.py
'''
import os
import sys
import json
# import cv2

cur_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(cur_dir,'../..')
sys.path.insert(0,os.path.join(root_dir,'src'))
sys.path.insert(0,os.path.join(root_dir,'run'))
from data.vibe_utils import *
from config import cfg

from tools.file_op import mkdir_safe
# update the  root_dir;
cfg.Engine.root_dir = root_dir
from tools.cam import set_camera
from pipeline import PipeLine

from toolkits import multi_view_render,multi_view_info_generator,load_pose_from_pare

if not os.path.exists(cfg.Engine.output_dir):
    cfg.Engine.output_dir =os.path.join(cfg.Engine.root_dir,cfg.Engine.output_dir)
    mkdir_safe(cfg.Engine.output_dir)




def load_pose_from_ACCAD(file_path):
    with np.load(file_path) as data:
        poses=data['poses']
        trans=data['trans']
        orient=data['root_orient']
        shapes=data['betas']

    return poses,trans,orient,shapes

# config

num_model=1
cfg.Engine.Model.selected = "SMPLX"
textures = '/home/swh/workspace/PG-engine/assets/smplx_texture_f_alb.png'
bg = '/home/swh/workspace/PG-engine/assets/background_test.jpg'
render=PipeLine(cfg,'debug', num_model,
                genders=['female'],
                textures=[textures],bg_img=bg)



pose_file = '/home/swh/dataset/smpl-data/ACCAD/s011/walkdog_stageii.npz'
trans_pose,trans_trans,trans_orient,trans_shapes=load_pose_from_ACCAD(pose_file)


for i in  range(2):
    pose = trans_pose[i].reshape(1,-1)
    shape = trans_shapes[:10].reshape(1,-1)
    t = trans_trans[i].reshape(1,-1)
    render.apply_input(pose=pose,shape=shape,trans=t,frame_info=i)


render.render()
