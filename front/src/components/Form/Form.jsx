import React, { useCallback, useEffect } from "react";
import "./Form.css";
import { useTelegram } from "../../hooks/useTelegram";
import { useState } from 'react';
import axios from 'axios';


const Form = () => {

    const [name, setName] = useState("");
    const [url, setUrl] = useState("");
    const [description, setDescription] = useState("");
    const [image, setImage] = useState(null); 
    const [imagePreview, setImagePreview] = useState("");
    const {tg} = useTelegram();

    const onSendData = useCallback(() => {

        const img_base64 = imagePreview.toString().split(',')[1];

        let body = new FormData();
        body.set('key', process.env.REACT_APP_API_KEY);
        body.set("image", img_base64);
        if (img_base64) {
            axios.post("https://api.imgbb.com/1/upload", body).then((res) => {
                const request = {
                    image : (res.data?.data?.url ? res.data?.data?.url : ""),
                    name,
                    url,
                    description
                };
                
                tg.sendData(JSON.stringify(request));
            })
        } else {
            const request = {
                image: "https://i.ibb.co/RhswWzs/images-q-tbn-ANd9-Gc-Rl-Dw9oz0w-ALjn-Jz2-MTmr-L2-Bp-E93f-Hk-LZW-2q-OPIBVFtlc-YXGFUBDIq-Si-Uajkk7-Naf.png",
                name,
                url,
                description
            };
            
            tg.sendData(JSON.stringify(request));
        }

    }, [name, url, description, imagePreview, tg]);

    useEffect(() => {
        tg.onEvent("mainButtonClicked", onSendData);
        return () => {
            tg.offEvent("mainButtonClicked", onSendData)
        }
    }, [onSendData, tg]);

    useEffect(() => {
        tg.MainButton.setParams({
            text: "Отправить",
        })
    }, [tg])

    useEffect(() => {
        if (!name || !url || !description) {
            tg.MainButton.hide();
        } else {
            tg.MainButton.show();
        }
    }, [name, url, description, tg])

    const onChangeName = (e) => {
        setName(e.target.value);
    }

    const onChangeUrl = (e) => {
        setUrl(e.target.value);
    }

    const onChangeDescription = (e) => {
        setDescription(e.target.value);
    }

    const onChangeImg = (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onloadend = () => {
            setImagePreview(reader.result);
          };
          reader.readAsDataURL(file);
          setImage(file);
        }
      };

    return (
        <div className={"form"}>
            <div className="Rectangle">
            <h3 style={{color: "#eee", fontSize: "24px"}}>Введите данные бота</h3>
            </div>
            <input 
                className = {"input"} 
                type = "text" 
                placeholder={"Название"}
                value = {name}
                onChange={onChangeName}
            />
            <input 
                className = {"input"} 
                type="text" 
                placeholder={"Адрес бота"}
                value = {url}
                onChange={onChangeUrl}
            />
            <input 
                className = {"input"} 
                type="text" 
                placeholder={"Описание"}
                value = {description}
                onChange={onChangeDescription}
            />
            {imagePreview && <img src={imagePreview} alt="Preview" style={{ width: '100px', height: '100px', marginTop: "20px", alignSelf: "center"}} />}
            <label class="input-file">
                <input 
                    type="file" 
                    accept="image/*"
                    onChange={onChangeImg} 
                /><span>Выберете файл</span></label>
        </div>
    )
}

export default Form;