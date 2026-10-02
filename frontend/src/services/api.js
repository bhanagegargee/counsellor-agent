import axios from "axios";


export const sendQuery = (query)=>{
  return axios.post("http://127.0.0.1:8000/api/admission/chat/",query);
}



