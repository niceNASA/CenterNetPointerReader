from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
import numpy as np
from progress.bar import Bar
import time
import torch
import math

try:
  from external.nms import soft_nms_39
except:
  print('NMS not imported! If you need it,'
        ' do \n cd $CenterNet_ROOT/src/lib/external \n make')
from models.decode import multi_pose_decode
from models.utils import flip_tensor, flip_lr_off, flip_lr
from utils.image import get_affine_transform
from utils.post_process import multi_pose_post_process
from utils.debugger import Debugger

from .base_detector import BaseDetector

def read_meter(bbox, C):
    print(bbox)
    # psx = bbox[5]
    # psy = 512 - bbox[6]
    # pex = bbox[7]
    # pey = 512 - bbox[8]

    # ssx = bbox[9]
    # ssy = 512 - bbox[10]
    # sex = bbox[11]
    # sey = 512 - bbox[12]

    # esx = bbox[13]
    # esy = 512 - bbox[14]
    # eex = bbox[15]
    # eey = 512 - bbox[16]
    psx = bbox[5]
    psy = bbox[6]
    pex = bbox[7]
    pey = bbox[8]

    ssx = bbox[9]
    ssy = bbox[10]
    sex = bbox[11]
    sey = bbox[12]

    esx = bbox[13]
    esy = bbox[14]
    eex = bbox[15]
    eey = bbox[16]

    if(pex == psx):
        angle_p = 90    #垂直的情况，防止除0错误
    else:
        k_p = (pey - psy)/(pex - psx)
        angle_p = math.degrees(math.atan(k_p))
    print(angle_p)

    if(sex == ssx):
        angle_s = 90
    else:
        k_s = (sey - ssy)/(sex - ssx)
        angle_s = math.degrees(math.atan(k_s))
    print(angle_s)

    if(eex == esx):
        angle_e = 90
    else:
        k_e = (eey - esy)/(eex - esx)
        angle_e = math.degrees(math.atan(k_e))
    print(angle_e)

    a = angle_p - angle_s
    b = angle_e - angle_s
    ratio = a/b
    print(ratio)
    #print(ratio * C)
    return ratio

class MultiPoseDetector(BaseDetector):
  def __init__(self, opt):
    super(MultiPoseDetector, self).__init__(opt)
    self.flip_idx = opt.flip_idx

  def process(self, images, return_time=False):
    with torch.no_grad():
      torch.cuda.synchronize()
      output = self.model(images)[-1]
      output['hm'] = output['hm'].sigmoid_()
      if self.opt.hm_hp and not self.opt.mse_loss:
        output['hm_hp'] = output['hm_hp'].sigmoid_()

      reg = output['reg'] if self.opt.reg_offset else None
      hm_hp = output['hm_hp'] if self.opt.hm_hp else None
      hp_offset = output['hp_offset'] if self.opt.reg_hp_offset else None
      torch.cuda.synchronize()
      forward_time = time.time()
      
      if self.opt.flip_test:
        output['hm'] = (output['hm'][0:1] + flip_tensor(output['hm'][1:2])) / 2
        output['wh'] = (output['wh'][0:1] + flip_tensor(output['wh'][1:2])) / 2
        output['hps'] = (output['hps'][0:1] + 
          flip_lr_off(output['hps'][1:2], self.flip_idx)) / 2
        hm_hp = (hm_hp[0:1] + flip_lr(hm_hp[1:2], self.flip_idx)) / 2 \
                if hm_hp is not None else None
        reg = reg[0:1] if reg is not None else None
        hp_offset = hp_offset[0:1] if hp_offset is not None else None
      
      dets = multi_pose_decode(
        output['hm'], output['wh'], output['hps'],
        reg=reg, hm_hp=hm_hp, hp_offset=hp_offset, K=self.opt.K)

    if return_time:
      return output, dets, forward_time
    else:
      return output, dets

  def post_process(self, dets, meta, scale=1):
    dets = dets.detach().cpu().numpy().reshape(1, -1, dets.shape[2])
    dets = multi_pose_post_process(
      dets.copy(), [meta['c']], [meta['s']],
      meta['out_height'], meta['out_width'])
    for j in range(1, self.num_classes + 1):
      dets[0][j] = np.array(dets[0][j], dtype=np.float32).reshape(-1, 17)
      # import pdb; pdb.set_trace()
      dets[0][j][:, :4] /= scale
      dets[0][j][:, 5:] /= scale
    return dets[0]

  def merge_outputs(self, detections):
    results = {}
    results[1] = np.concatenate(
        [detection[1] for detection in detections], axis=0).astype(np.float32)
    if self.opt.nms or len(self.opt.test_scales) > 1:
      soft_nms_39(results[1], Nt=0.5, method=2)
    results[1] = results[1].tolist()
    return results

  def debug(self, debugger, images, dets, output, scale=1):
    dets = dets.detach().cpu().numpy().copy()
    dets[:, :, :4] *= self.opt.down_ratio
    dets[:, :, 5:17] *= self.opt.down_ratio
    img = images[0].detach().cpu().numpy().transpose(1, 2, 0)
    img = np.clip(((
      img * self.std + self.mean) * 255.), 0, 255).astype(np.uint8)
    pred = debugger.gen_colormap(output['hm'][0].detach().cpu().numpy())
    debugger.add_blend_img(img, pred, 'pred_hm')
    if self.opt.hm_hp:
      pred = debugger.gen_colormap_hp(
        output['hm_hp'][0].detach().cpu().numpy())
      debugger.add_blend_img(img, pred, 'pred_hmhp')
  
  def show_results(self, debugger, image, results, path_name):
    # 从路径中截取源文件名称
    index1 = path_name.rfind('\\') + 1
    index2 = path_name.rfind('.') 
    file_name = path_name[index1:index2]
    #debugger.add_img(image, img_id='multi_pose')
    debugger.add_img(image, img_id=file_name)
    ra = 0
    for bbox in results[1]:
      if bbox[4] > self.opt.vis_thresh:
        ra = read_meter(bbox, 60)
        #debugger.add_coco_bbox(bbox[:4], 0, bbox[4], img_id='multi_pose')
        # debugger.add_coco_bbox(bbox[:4], 0, ra, img_id='multi_pose')
        # debugger.add_coco_hp(bbox[5:17], img_id='multi_pose')
        #print(bbox)
        debugger.add_coco_bbox(bbox[:4], 0, ra, img_id=file_name)
        debugger.add_coco_hp(bbox[5:17], img_id=file_name)
        
    #debugger.show_all_imgs(pause=self.pause)
    file = open("D:\\workspace\\pointerHandler\\pointerHandler\\upload\\result.txt", "w+")
    ra1 = abs(ra)
    tmp = str(round(ra1*100)) + "%"
    file.write(tmp)
    file.close()
    #debugger.save_all_imgs()
    #debugger.save_img(file_name)
    debugger.save_img_upload(file_name)