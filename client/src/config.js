import { config } from "dotenv";
config();

export const PORT = 8000
export const HOST = "localhost"
export const URL = `http://${HOST}:${PORT}`

export const ACCESS_TOKEN = process.env.REACT_APP_ACCESS_TOKEN;
export const PUBLIC_KEY = process.env.REACT_APP_PUBLIC_KEY;
