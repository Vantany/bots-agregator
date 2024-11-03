import React, { useCallback, useEffect } from "react";
import "./Form.css";
import { useTelegram } from "../../hooks/useTelegram";
import { useState } from 'react';


const Form = () => {

    const [name, setName] = useState("");
    const [url, setUrl] = useState("");
    const [description, setDescription] = useState("");  
    const {tg} = useTelegram();

    const onSendData = useCallback(() => {
        const data = {
            name,
            url,
            description
        }
        tg.sendData(JSON.stringify(data));
    }, [name, url, description]);

    useEffect(() => {
        tg.onEvent("mainButtonClicked", onSendData);
        return () => {
            tg.offEvent("mainButtonClicked", onSendData)
        }
    }, [onSendData]);

    useEffect(() => {
        tg.MainButton.setParams({
            text: "Отправить",
        })
    }, [])

    useEffect(() => {
        if (!name || !url || !description) {
            tg.MainButton.hide();
        } else {
            tg.MainButton.show();
        }
    }, [name, url, description])

    const onChangeName = (e) => {
        setName(e.target.value);
    }

    const onChangeUrl = (e) => {
        setUrl(e.target.value);
    }

    const onChangeDescription = (e) => {
        setDescription(e.target.value);
    }

    return (
        <div className={"form"}>
            <h3>Введите данные бота</h3>
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
        </div>
    )
}

export default Form;