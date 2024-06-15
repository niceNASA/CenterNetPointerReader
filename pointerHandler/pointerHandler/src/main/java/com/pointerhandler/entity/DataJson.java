package com.pointerhandler.entity;

import java.util.Map;

public class DataJson {
    private Integer code;
    private String msg;
    private Map<String, String> data;
    private Integer startrange;
    private Integer endrange;

    public Integer getCode() {
        return code;
    }

    public void setCode(Integer code) {
        this.code = code;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public Map<String, String> getData() {
        return data;
    }

    public void setData(Map<String, String> data) {
        this.data = data;
    }

    public Integer getStartrange() {
        return startrange;
    }

    public void setStartrange(Integer startrange) {
        this.startrange = startrange;
    }

    public Integer getEndrange() {
        return endrange;
    }

    public void setEndrange(Integer endrange) {
        this.endrange = endrange;
    }
//    @Override
//    public String toString() {
//        return "DataJson{" +
//                "code=" + code +
//                ", msg='" + msg + '\'' +
//                ", data=" + data +
//                '}';
//    }


    @Override
    public String toString() {
        return "DataJson{" +
                "code=" + code +
                ", msg='" + msg + '\'' +
                ", data=" + data +
                ", startrange=" + startrange +
                ", endrange=" + endrange +
                '}';
    }
}
