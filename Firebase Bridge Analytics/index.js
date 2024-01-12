/**
 * Import function triggers from their respective submodules:
 *
 * const {onCall} = require("firebase-functions/v2/https");
 * const {onDocumentWritten} = require("firebase-functions/v2/firestore");
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

const functions = require("firebase-functions");
const admin = require("firebase-admin");
const axios = require("axios");
const API_KEY = ""; // I have removed the API key to avoid leaks, because project is already deployed

admin.initializeApp();

// Create and deploy your first functions
// https://firebase.google.com/docs/functions/get-started

const axiosInstanceGPT = axios.create({
    baseURL: "https://api.openai.com/v1/",
    headers: {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": `Bearer ${API_KEY}`,
    },
});

exports.saveAnalytics = functions.https.onRequest((req, res) => {
    const data = req.query.data;
    const period = req.query.period;
    const userId = req.query.userId;

    const prompt = "Ты находишься в приложении Яндекс Алиса и представляешь собой интерактивного помощника по продуктивной деятельности. Тебе нужно создать краткую аналитику и общие рекомендации на основе данных деятельности за период (" + period + ") пользователя, который пользователь фиксирует в течении данного периода. Свой ответ пришли без форматирования (например, без жирного шрифта), максимум 6 предложений. Начало ответа формируй со словами 'Я Накопитель сформировал аналитику для Вас'. Ниже представлены данные: \n" + data;
    const path = "Yandex/" + userId;

    const container = {
        model: "gpt-3.5-turbo",
        messages: [
            { role: "user", content: prompt },
        ],

        max_tokens: 512,
        temperature: 0.6,
    };


    res.status(200).send();
    try {
        const result = axiosInstanceGPT.post("chat/completions", container).then(result => {
            //return res.status(200).send(result.data.choices[0].message.content);
            //return result.data.choices[0].message.content;
            const dataAnalytics = result.data.choices[0].message.content;
            admin.database().ref(path).set(dataAnalytics);
        });
    } catch (error) {
        console.error("Error while fetching completion:", error.message);
        throw error;
    }
});

exports.getAnalytics = functions.https.onRequest((req, res) => {
    const userId = req.query.userId;
    const path = "Yandex/" + userId;

    
    admin.database().ref(path).once("value").then(dataAnalytics => {
        if (dataAnalytics.exists()) {
            return res.status(200).send(dataAnalytics.val());
        } else {
            return res.status(200).send('600');
        }
    });
});

exports.GPT = functions.https.onRequest((req, res) => {
    const data = req.query.data;
    const period = req.query.period;
    const userId = req.query.userId;

    const prompt = "Ты находишься в приложении Яндекс Алиса и представляешь собой интерактивного помощника по продуктивной деятельности. Тебе нужно создать краткую аналитику и общие рекомендации на основе данных деятельности за период (" + period + ") пользователя, который пользователь фиксирует в течении данного периода. Свой ответ пришли без форматирования (например, без жирного шрифта), максимум 6 предложений. Начало ответа формируй со словами 'Я Накопитель сформировал аналитику для Вас'. Ниже представлены данные: \n" + data;

    const container = {
        model: "gpt-3.5-turbo",
        messages: [
            { role: "user", content: prompt },
        ],

        max_tokens: 512,
        temperature: 0.6,
    };

    try {
        const result = axiosInstanceGPT.post("chat/completions", container).then(result => {
            return res.status(200).send(result.data.choices[0].message.content); 
        });
    } catch (error) {
        console.error("Error while fetching completion:", error.message);
        throw error;
    }
});

