package com.pointerhandler.utils;

import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.util.UUID;

public class UploadUtils {
    //定义目标路径
    private static final String BASE_PATH = "D:\\workspace\\pointerHandler\\pointerHandler\\upload";

    //定义图片访问路径
    private static final String SERVER_PATH = "http://localhost:8080/upload/";

    public static String upload(MultipartFile file){
        //获得上传文件的原始名称
        String filename = file.getOriginalFilename();
        //保证上传图片名称的唯一性
        String uuid = UUID.randomUUID().toString().replace("-", "");
        String newFileName = uuid + "-" + filename;
        //创建一个文件实例对象
        File image = new File(BASE_PATH, newFileName);
        if(!image.exists()){
            image.mkdirs();
        }
        try {
            file.transferTo(image);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }

        return newFileName;
    }
}
