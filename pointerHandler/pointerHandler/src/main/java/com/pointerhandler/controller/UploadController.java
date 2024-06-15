package com.pointerhandler.controller;

import com.pointerhandler.entity.DataJson;
import com.pointerhandler.utils.UploadUtils;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.multipart.MultipartFile;


import java.io.*;
import java.util.HashMap;

@Controller
@RequestMapping("upload")
public class UploadController {

    @RequestMapping("image")
    @ResponseBody
    public DataJson uploadImage(@RequestParam(value = "file") MultipartFile multipartFile){
        //调用上传工具类
        String imagePath = UploadUtils.upload(multipartFile);

        DataJson dataJson = new DataJson();
        if(imagePath != null){
            dataJson.setCode(1);
            dataJson.setMsg("上传成功");
            HashMap<String, String> map = new HashMap<>();
            map.put("src",imagePath);
            dataJson.setData(map);
        }else{
            dataJson.setCode(0);
            dataJson.setMsg("上传失败");
        }
        return dataJson;
    }

    @RequestMapping("process")
    @ResponseBody
    public DataJson process(String serverImagePath, int startrange, int endrange) throws FileNotFoundException {
        System.out.println("当前路径：" + serverImagePath);
        System.out.println(startrange);
        System.out.println(endrange);
        //runCmd("conda activate centernet1");
        String cmd = "python D:\\workspace\\CenterNetReadGPU\\CenterNet\\src\\demo.py multi_pose --demo " +
                "D:\\workspace\\pointerHandler\\pointerHandler\\upload\\" + serverImagePath +
                " --load_model D:\\workspace\\CenterNetReadGPU\\CenterNet\\models\\model_best.pth --dataset pointer512";
        System.out.println(cmd);
        String returnValue = runCmd(cmd);
        DataJson dataJson = new DataJson();
        if(serverImagePath != null){
            dataJson.setCode(1);

            String filePath = "D:\\workspace\\pointerHandler\\pointerHandler\\upload\\result.txt";
            String str = null;
            try {
                BufferedReader in = new BufferedReader(new FileReader(filePath));
                str = in.readLine();
            } catch (IOException e) {
                e.printStackTrace();
            }

            dataJson.setMsg(str);
            HashMap<String, String> map = new HashMap<>();
            map.put("src","multi_pose.png");
            dataJson.setData(map);
            dataJson.setStartrange(startrange);
            dataJson.setEndrange(endrange);
        }else{
            dataJson.setCode(0);
            dataJson.setMsg("上传失败");
        }
        return dataJson;
    }

    public static String runCmd(String command) {
        Process process = null;
        String returnValue = "";
        try {
            process = Runtime.getRuntime().exec(command);
            BufferedReader reader = new BufferedReader(
                    new InputStreamReader(
                            process.getInputStream()));
            String data = "";
            while((data = reader.readLine()) != null) {
                System.out.println(data);
                returnValue = returnValue.concat(data);
            }

            int exitValue = process.waitFor();

            if(exitValue != 0) {
                System.out.println("error");
            }
        } catch(Exception e) {
            e.printStackTrace();
        }

        return returnValue;
    }

}
